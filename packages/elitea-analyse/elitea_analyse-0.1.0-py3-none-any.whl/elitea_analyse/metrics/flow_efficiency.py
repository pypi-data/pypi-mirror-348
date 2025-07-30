""" This module contains the FlowEfficiencyMetric class. """
import pandas as pd

from src.metrics.status_based_metric import StatusBasedMetric
from src.metrics.constants import CLOSED, FLOW_EFFICIENCY
from src.utils.constants import WAITING_FOR_RELEASE_STATUS
# pylint: disable=attribute-defined-outside-init


class FlowEfficiencyMetric(StatusBasedMetric):
    """
    This class calculates the flow efficiency metric.
    """
    def __init__(self, work_items: pd.DataFrame, statuses_mapping: pd.DataFrame,
                 basic_columns_to_group_by: list = None, aggregate_by: list = None):
        work_items = self._filter_items(work_items, (work_items['request_type'] == CLOSED))\
            .query(f"status_history != '{WAITING_FOR_RELEASE_STATUS}'")
        self.column_name = FLOW_EFFICIENCY
        super().__init__(work_items, statuses_mapping, basic_columns_to_group_by, aggregate_by)

    def calculate(self) -> pd.DataFrame:
        """
        Calculate and return the flow efficiency as a ratio of time closed items spent in active statuses to their
        lead time per closed year-month, project, team and issue type.
        """
        if (res := super().calculate()) is not None:
            return res

        df_merged = self.work_items.merge(self.statuses_mapping, left_on='status_history', right_on='status_raw')
        df_active_waiting_time = df_merged.pivot_table(
            index=self.columns_to_group_by + ['issue_id'],  values='time_in_status',
            columns='status_type', aggfunc='sum').reset_index()
        df_active_waiting_time.loc[:, 'Active'] = df_active_waiting_time.loc[:, 'Active'].fillna(0)
        df_active_waiting_time['total_time'] = df_active_waiting_time['Active'] + df_active_waiting_time['Waiting']

        df_active_waiting_time[self.column_name] = (
                df_active_waiting_time['Active']/df_active_waiting_time['total_time'])
        col_agg_dict = self._consruct_column_names_based_on_agg(self.column_name, self.aggregate_by)
        df_active_waiting_time = self._duplicate_columns(
            df_active_waiting_time, self.column_name, col_agg_dict.keys())
        self.metric_df = df_active_waiting_time.groupby(self.columns_to_group_by).agg(col_agg_dict).reset_index()
        self.metric_df = self.metric_df.rename(columns={self.column_name + '_mean': self.column_name})
        return self.metric_df
