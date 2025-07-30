"""This module retrieves a database credentials and Jira service account credentials from AWS Secret Manager."""

import json
import logging
import boto3

from botocore.exceptions import ClientError


class SecretManagerRetrieve:
    """
    A class to retrieve secrets' values from AWS Secret manager.

    Attributes:
        secret_id: str
            ID of the secret with database credentials (user and password).
    """

    def __init__(self, secret_id: str, region: str):
        self.secret_id = secret_id
        try:
            self.secretsmanager = boto3.client('secretsmanager', region)
        except ClientError as err:
            logging.exception(err.response)
            raise err

    def get_db_credentials(self) -> tuple:
        """Get a db credentials."""
        secret_data = self.get_secret_data()
        logging.info('Database credentials has been retrieved from the Secret Manager.')
        return secret_data.get('username'), secret_data.get('password')

    def get_jira_credentials(self) -> tuple:
        """Get credentials for Jira connection."""
        secret_data = self.get_secret_data()
        logging.info('Jira credentials has been retrieved from the Secret Manager.')
        return secret_data.get('jira-url'), secret_data.get('jira-user'), secret_data.get('jira-token')

    def get_secret_data(self) -> dict:
        """Get secrets' data from AWS Secret Manager."""
        response = self.secretsmanager.get_secret_value(SecretId=self.secret_id)
        secret_data = response['SecretString']
        return json.loads(secret_data)
