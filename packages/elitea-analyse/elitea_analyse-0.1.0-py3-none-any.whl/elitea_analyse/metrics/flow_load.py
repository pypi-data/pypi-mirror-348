""" This module contains the FlowLoadMetric class. """
from typing import Callable
from calendar import monthrange
from math import ceil

import pandas as pd

from src.metrics.base_metric import BaseMetric
from src.metrics.constants import YEAR_MONTH, CLOSED, FLOW_LOAD, OPEN
from src.utils.constants import WAITING_FOR_RELEASE_STATUS
# pylint: disable=attribute-defined-outside-init


class FlowLoadMetric(BaseMetric):
    """
    This class calculates the flow efficiency metric.
    """
    def __init__(self, work_items: pd.DataFrame, basic_columns_to_group_by: list = None):
        work_items = work_items.query(
            f"request_type in ['{CLOSED}', '{OPEN}'] & status_history != '{WAITING_FOR_RELEASE_STATUS}'")
        super().__init__(work_items, basic_columns_to_group_by)
        self.column_name = FLOW_LOAD
        if YEAR_MONTH not in self.columns_to_group_by:
            self.columns_to_group_by.append(YEAR_MONTH)

    def calculate(self) -> pd.DataFrame:
        """
        Calculate and return the flow load as a number of items WIP per calendar month, which includes both open and
        closed items.
        """
        if (res := super().calculate()) is not None:
            return res

        df_items_state_per_day = pd.DataFrame()
        for project in self.work_items['project_name'].unique().tolist():
            df_history_one_project = self.work_items[self.work_items['project_name'] == project]
            if df_history_one_project[df_history_one_project['request_type'] == CLOSED].empty:
                continue
            dates_interval = self._define_dates_interval(df_history_one_project, 'resolved_date')
            df_joined = self._cross_join_work_items_and_calendar(dates_interval, df_history_one_project)
            df_items_state_per_day = pd.concat([df_items_state_per_day, df_joined])
        df_items_state_per_day.loc[:, YEAR_MONTH] = df_items_state_per_day['calendar_days'].dt.to_period('M')
        self.metric_df = df_items_state_per_day.groupby(self.columns_to_group_by).agg({'issue_id': 'nunique'})
        self.metric_df = self.metric_df.rename(columns={'issue_id': self.column_name}).reset_index()
        return self.metric_df

    def _define_dates_interval(self, df_input: pd.DataFrame, date_column_name: str) -> tuple:
        """
        Calculate the minimum and maximum dates in the specified date column of the input DataFrame and return as the
        first and the last day of a month.
        If both min and max dates exist, it returns a tuple of these dates.
        If either of the dates does not exist, it returns a tuple of today's date and the date a year ago.
        """
        if df_input.empty:
            return tuple()
        df_input[date_column_name] = pd.to_datetime(df_input[date_column_name])
        start_date = df_input[date_column_name].min().date().replace(day=1)
        end_date = df_input[date_column_name].max().date().replace(day=1)
        if not pd.isnull(end_date):
            end_date = end_date.replace(day=monthrange(end_date.year, end_date.month)[1])
        return start_date, end_date

    def _cross_join_work_items_and_calendar(self, dates_interval: tuple, df_items: pd.DataFrame) -> pd.DataFrame:
        """
        Cross join work items data and calendar to get information on the historical statuses for every day in
        the defined period.
        """
        df_dates = self._generate_dates_dataframe(dates_interval)
        return self._process_dataframe_in_chunks(df_items, lambda chunk: self._cross_join_and_filter(df_dates, chunk))

    def _generate_dates_dataframe(self, dates_interval: tuple) -> pd.DataFrame:
        """Generate a dataframe with one column, which contains calendar days."""
        start_date, end_date = dates_interval
        calendar_days = pd.date_range(start_date, end_date)
        return pd.DataFrame(calendar_days, columns=['calendar_days'])

    def _cross_join_and_filter(self, df_dates: pd.DataFrame, df_items: pd.DataFrame) -> pd.DataFrame:
        df_merged = pd.merge(df_dates, df_items, how='cross')
        return df_merged[(df_merged['calendar_days'] >= df_merged['from_date'])
                         & (df_merged['calendar_days'] <= df_merged['to_date'])]

    def _process_dataframe_in_chunks(self, df_input: pd.DataFrame,
                                     process_function: Callable[[pd.DataFrame], pd.DataFrame],
                                     chunk_size: int = 10000) -> pd.DataFrame:
        """
        This function divides the input DataFrame into chunks of a specified size and applies a given function to each
        chunk. The results are then concatenated into a single DataFrame and returned.
        """
        num_chunks = ceil(len(df_input) / chunk_size)
        df_result = pd.DataFrame()
        for i in range(num_chunks):
            start_row = i * chunk_size
            end_row = (i + 1) * chunk_size
            chunk = df_input.iloc[start_row:end_row]
            df_intermediate = process_function(chunk)
            df_result = pd.concat([df_result, df_intermediate])
        return df_result
