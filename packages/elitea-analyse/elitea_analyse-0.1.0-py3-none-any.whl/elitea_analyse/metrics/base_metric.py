""" This module contains the abstract class BaseMetric """
from abc import ABC, abstractmethod
import logging
import pandas as pd


class BaseMetric(ABC):
    """
    This is an abstract class that should be inherited by all classes that calculate metrics.
    Every inherited class should implement the calculate method that calculates the metric.
    """
    items_columns_to_check = {
        'issue_id', 'issue_key', 'issue_type', 'project_key', 'project_name', 'team', 'resolution',
        'status', 'created_date', 'resolved_date', 'status_history', 'time_in_status',
    }

    def __init__(self, work_items: pd.DataFrame, basic_columns_to_group_by: list = None,
                 aggregate_by: list = None):
        self.work_items = work_items

        if not basic_columns_to_group_by:
            basic_columns_to_group_by = self._list_columns_to_group_by()
        self.columns_to_group_by = basic_columns_to_group_by
        self.aggregate_by = aggregate_by or ['mean']
        self.metric_df = pd.DataFrame()
        self._check_input_dataframe()
        self._check_dates_columns()

    @abstractmethod
    def calculate(self) -> pd.DataFrame:
        """
        Calculates the metric and returns the result as a DataFrame.
        """
        if not self.metric_df.empty:
            return self.metric_df

        if self.work_items.empty:
            logging.info('There is no work items for the metrics calculation.')
            return self.metric_df

        return None

    def _list_columns_to_group_by(self) -> list:
        """
        Creates basic list of columns that metrics output should contain. If data has been extracted from Jira
        it contains values in the column projects_key, and it is added to the list. But, if data has been extracted
        from ADO it does not contain projects_key (only project_name).
        """
        group_by_list = ['project_name', 'issue_type']
        if not self.work_items['project_key'].isnull().values.all():
            group_by_list.extend(['project_key'])
        if not self.work_items['team'].isnull().values.all():
            group_by_list.extend(['team'])
        return group_by_list

    def _filter_items(self, df: pd.DataFrame, condition) -> pd.DataFrame:
        """
        Keep only closed work items in the input work items dataframe.
        """
        filtered_items = df[condition]
        if filtered_items.empty:
            logging.info(f'There is no work items that would match a condition {condition}.')
        return filtered_items

    def _check_input_dataframe(self):
        """
        Check if the input dataframe contains all the necessary columns.
        """
        check_list, input_list = self.items_columns_to_check, set(self.work_items.columns)
        if not check_list.issubset(input_list):
            raise KeyError(f'The columns {list(check_list - input_list)} are missing in your dataset!')

    def _check_dates_columns(self) -> pd.DataFrame:
        """
        Check and convert the 'created_date' and 'resolved_date' columns to datetime format if they are not already.
        """
        for column in ['created_date', 'resolved_date', 'from_date', 'to_date']:
            if self.work_items[column].dtype == 'object':
                self.work_items[column] = pd.to_datetime(self.work_items[column], errors='coerce')
        return self.work_items

    def _consruct_column_names_based_on_agg(self, column: str, agg_funcs: list) -> dict:
        """
        Construct column names based on the columns and aggregation functions.
        Names are constructed as {column_base_name}_{agg_func}.
        """
        if 'mean' not in agg_funcs:
            agg_funcs.extend(['mean'])
        return {f'{column}_{agg}': agg for agg in agg_funcs}

    def _duplicate_columns(self, df: pd.DataFrame, column: str, new_columns: list) -> pd.DataFrame:
        """
        Duplicate column to new_columns in the dataframe.
        """
        for new_column in new_columns:
            df[new_column] = df[column]
        return df
