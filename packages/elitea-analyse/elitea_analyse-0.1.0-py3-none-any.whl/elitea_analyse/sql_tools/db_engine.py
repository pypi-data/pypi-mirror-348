"""This module connects to a SQL database and performs CRUD operations."""

import logging

from typing import Any, Optional, Literal
from collections.abc import Generator
from contextlib import contextmanager
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.exc import OperationalError, ProgrammingError

from retry import retry
import pandas as pd

from ..azure.get_key_vault_secret import get_secret
from ..aws.read_secret import SecretManagerRetrieve
from ..utils.read_config import Config
from ..utils.circuit_breaker import CircuitBreaker, CircuitOpenException


class DBEngine:
    """
    A class to connect to a DataBase and perform CRUD operations.

    Attributes:
        config_path: str
            one or more projects keys separated with comma.
        cloud_provider: str
            a cloud provider name.
        db_cfg: dict
            a dictionary with DB configuration (host, port, name), which stored in a YML file.
        db_user, db_password: str
            a DB user and password, retrieved from the AWS Secret Manager.
        engine: a new class: _engine.Engine instance
            the core of database connectivity and transaction management in the context of SQLAlchemy.
    """

    def __init__(self, config_path: str, cloud_provider: str):
        self.cloud_provider = cloud_provider
        if cloud_provider not in ['aws', 'azure']:
            raise ValueError('cloud must be either "aws" or "azure"')
        self.config_path = config_path
        self.db_cfg = Config.read_config(self.config_path)['DataBase']
        self.db_user, self.db_password = self.__get_user()
        self.engine = self.__create_engine()

    def __get_user(self) -> Optional[tuple]:
        """Get a DataBase username and password from the AWS Secret Manager."""
        db_user, db_password = None, None
        if self.cloud_provider == 'azure':
            secret_cfg = Config.read_config(self.config_path)['KeyVault']
            db_secrets = secret_cfg['db_credentials']
            db_user = get_secret(secret_cfg['key_vault_url'], db_secrets['db_user'])
            db_password = get_secret(secret_cfg['key_vault_url'], db_secrets['db_password'])
        elif self.cloud_provider == 'aws':
            secret_cfg = Config.read_config(self.config_path)['SecretsIds']
            db_user, db_password = SecretManagerRetrieve(secret_cfg['db_credentials'],
                                                         self.db_cfg['region']).get_db_credentials()
        return db_user, db_password

    def __create_engine(self) -> Engine:
        """Create an SQL Alchemy Engine instance."""
        conn_str = ''
        if self.cloud_provider == 'aws':
            conn_str = (f'mysql+pymysql://{self.db_password}@{self.db_cfg["db_host"]}:{self.db_cfg["db_port"]}'
                        f'{self.db_cfg["db_name"]}')
        elif self.cloud_provider == 'azure':
            conn_str = (f'mssql+pyodbc://{self.db_user}:{self.db_password}@{self.db_cfg["server"]}/'
                        f'{self.db_cfg["db_name"]}?driver=ODBC+Driver+18+for+SQL+Server')
        try:
            return create_engine(conn_str)
        except OperationalError as err:
            logging.info('Error creating db engine: %s', err)
            raise err

    @retry((OperationalError, CircuitOpenException), tries=4, delay=2, backoff=2)
    @CircuitBreaker(max_failures=3, reset_timeout=5)
    def write_to_db(self, df_input: pd.DataFrame, db_table_name: str, write_mode: Literal['replace', 'append']):
        """Upload data from a DataFrame to a DataBase. """
        if df_input.empty:
            logging.info('No data to write to the database.')
            return
        with self.get_connection() as conn:
            with conn.begin() as transaction:  # pylint: disable=E1101
                with self.handle_database_errors(db_table_name, conn, transaction):
                    df_input.index.names = ['id']
                    df_input.to_sql(name=db_table_name, con=self.engine, if_exists=write_mode)
                    logging.info('DataFrame written to the %s table in the RDS database.', db_table_name)

    @retry((OperationalError, CircuitOpenException), tries=4, delay=2, backoff=2)
    @CircuitBreaker(max_failures=3, reset_timeout=5)
    def get_field_unique_values(self, db_table_name: str, column_name: str, condition: str) -> list:
        """Get a list of unique values in a DataBase column."""
        with self.get_connection() as conn:
            with self.handle_database_errors(db_table_name, conn):
                query = conn.execute(text(
                    f'SELECT DISTINCT {column_name} FROM {db_table_name} '
                    f'WHERE {condition} ORDER BY {column_name} DESC'))
                logging.info('%s unique values extracted from the table %s.', column_name, db_table_name)
                unique_values = []
                for row in query:
                    try:
                        value_str = str(getattr(row, column_name))
                        unique_values.append(value_str)
                    except ValueError as err:
                        logging.info('Error converting value to string: %s', err)
                        raise err
                return unique_values

    @retry((OperationalError, CircuitOpenException), tries=4, delay=2, backoff=2)
    @CircuitBreaker(max_failures=3, reset_timeout=5)
    def del_rows(self, db_table_name: str, condition: str):
        """Delete data from a DataBase table based on some condition."""
        if not condition:
            logging.info('No condition for deletion has been provided.')
            return
        with self.get_connection() as conn:
            with conn.begin() as transaction:  # pylint: disable=E1101
                with self.handle_database_errors(db_table_name, conn, transaction):
                    conn.execute(text(f'DELETE FROM {db_table_name} WHERE {condition}'))
                    logging.info('Data has been deleted from the table %s', db_table_name)

    @retry((OperationalError, CircuitOpenException), tries=4, delay=2, backoff=2)
    @CircuitBreaker(max_failures=3, reset_timeout=5)
    def select_and_upload_to_df(self, db_table_name: str, condition: str) -> pd.DataFrame:
        """Select data from a DataBase table based on some condition and upload it to a DataFrame."""
        if not condition:
            logging.info('No condition for selection has been provided.')
            return pd.DataFrame()
        with self.get_connection() as conn:
            with self.handle_database_errors(db_table_name, conn):
                query = conn.execute(text(f'SELECT * FROM {db_table_name} WHERE {condition}'))
                logging.info('Data has been selected from the table %s', db_table_name)
                return pd.DataFrame(query.fetchall(), columns=query.keys())

    @contextmanager
    def get_connection(self):
        """Create a connection to the DataBase."""
        connection = self.engine.connect()
        try:
            yield connection
        finally:
            connection.close()

    @staticmethod
    @contextmanager
    def handle_database_errors(db_table_name: str, connection: Any = None,
                               transaction: Any = None) -> Generator[None, None, None]:
        """Handle DataBase exceptions."""
        try:
            yield
            if transaction:
                transaction.commit()
        except OperationalError as err:
            logging.info('Cannot connect to DB: %s', str(err))
            if transaction:
                transaction.rollback()
            raise err
        except ProgrammingError as err:
            logging.info('NoSuchTableError: The %s table does not exist in the database.', db_table_name)
            if transaction:
                transaction.rollback()
            raise err
        except Exception as err:  # pylint: disable=broad-except
            logging.info('An error occurred: %s', str(err))
            if transaction:
                transaction.rollback()
        finally:
            if connection and not connection.closed:
                connection.close()
