"""
This module to transform Tasks' data extracted form Click Up.
"""
from typing import Optional
from datetime import datetime

import pandas as pd

from src.utils.convert_to_datetime import unix_milliseconds_to_datetime


class ClickUpTransform:
    """
    A class to transform extracted data from ClickUP (tasks and time in status data).

    Attributes:
        df_tasks: pd.Dataframe
            tasks data;
        df_time_in_status: pd.Dataframe
            time in status data for all the tasks.
    """

    def __init__(self, df_tasks, df_time_in_status):
        self.df_tasks = df_tasks
        self.df_time_in_status = df_time_in_status

    def transform_data(self, data_extraction_date: datetime) -> pd.DataFrame:
        """Apply all transformation steps and final tasks' dataset for analysis."""
        self.df_tasks[['project_key', 'resolution', 'labels', 'components', 'start_date', 'defects_environment']] = None
        self.df_tasks['request_type'] = self.df_tasks.apply(lambda x: self.add_request_type(x['closed_date']), axis=1)
        self.convert_date_and_time_values()
        self.add_status_end_date(data_extraction_date)
        return self.df_tasks.merge(self.df_time_in_status, how='left', on='issue_id')

    def add_status_end_date(self, data_extraction_date: datetime) -> None:
        """
        Add information on statuses' end dates:
        - for intermediate statuses their end date is the start date of the next task's status;
        - for the final status it's end date is the date of the data extraction if a task is open or None if closed.
        """
        self.df_time_in_status = self.df_time_in_status.sort_values(by=['issue_id', 'from_date'], ignore_index=True)
        df_dates_shifted = self.df_time_in_status.reset_index()[['index', 'issue_id', 'from_date']]
        df_dates_shifted['index_new'] = df_dates_shifted['index'] - 1
        self.df_time_in_status = self.df_time_in_status.merge(
            df_dates_shifted, how='left', left_index=True, right_on='index_new', suffixes=('', '_shifted'))

        self.df_time_in_status['to_date'] = self.df_time_in_status.apply(
            lambda x: self.get_status_end_date(
                x['type'], x['from_date_shifted'], x['issue_id'], x['issue_id_shifted'], data_extraction_date),
            axis=1)
        self.df_time_in_status = self.df_time_in_status.rename(columns={'status': 'status_history'})
        self.df_time_in_status = self.df_time_in_status[
            ['issue_id', 'status_history', 'from_date', 'to_date', 'time_in_status', 'type']]

    @staticmethod
    def get_status_end_date(request_type: str, from_date_shifted: datetime, task_id: str, task_id_shifted: str,
                            data_extraction_date: datetime) -> Optional[datetime]:
        """
        Define end date for a task's historical status based on the initial date of the next
        historical status and status type.
        """
        if task_id != task_id_shifted and request_type == 'closed':
            return None
        if task_id == task_id_shifted:
            return from_date_shifted
        if task_id != task_id_shifted and request_type == 'open':
            return data_extraction_date
        return None

    def convert_date_and_time_values(self) -> None:
        """
        Convert:
         - time in status for tasks from minutes to days;
         - status start date from Unix (milliseconds) to datetime.
        """
        self.df_time_in_status['time_in_status'] = self.df_time_in_status['total_time.by_minute'] / 60 / 24
        self.df_time_in_status['from_date'] = self.df_time_in_status.apply(
            lambda x: unix_milliseconds_to_datetime(x['total_time.since']), axis=1)

    @staticmethod
    def add_request_type(closed_date: datetime) -> str:
        """Define if the task is closed based on the value of its closure date."""
        if pd.isnull(closed_date):
            return 'open'
        return 'closed'
