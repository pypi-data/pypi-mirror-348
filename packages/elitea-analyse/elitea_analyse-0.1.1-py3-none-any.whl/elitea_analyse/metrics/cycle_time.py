""" This module contains the CycleTimeMetric class. """
import logging
import pandas as pd

from src.metrics.status_based_metric import StatusBasedMetric
from src.metrics.constants import CYCLE_TIME, CLOSED
from src.utils.constants import WAITING_FOR_RELEASE_STATUS
# pylint: disable=attribute-defined-outside-init


class CycleTimeMetric(StatusBasedMetric):
    """
    This class calculates the cycle time metric.
    """
    def __init__(self, work_items: pd.DataFrame, statuses_mapping: pd.DataFrame,
                 basic_columns_to_group_by: list = None, aggregate_by: list = None):
        work_items = self._filter_items(work_items, (work_items['request_type'] == CLOSED))\
            .query(f"status_history != '{WAITING_FOR_RELEASE_STATUS}'")
        self.column_name = CYCLE_TIME
        super().__init__(work_items, statuses_mapping, basic_columns_to_group_by, aggregate_by)

    def calculate(self) -> pd.DataFrame:
        """
        Calculate and return the cycle time for the given items that have statuses in cycle time.
        """
        if (res := super().calculate()) is not None:
            return res

        statuses_in_cycle_tyme = self.statuses_mapping[
            self.statuses_mapping['add_to_cycle_time'] == 'y']['status_raw'].tolist()
        if not statuses_in_cycle_tyme:
            logging.info('There is no statuses marked as add_to_cycle_time.')
            return pd.DataFrame()

        self.metric_df = self.work_items[self.work_items['status_history'].isin(statuses_in_cycle_tyme)]
        self.metric_df = self.metric_df.pivot_table(index='issue_id', values='time_in_status', aggfunc='sum')
        self.metric_df = self.metric_df.reset_index().rename(columns={'time_in_status': self.column_name})
        self.metric_df = self.work_items.drop_duplicates(subset=['issue_id'])\
            .merge(self.metric_df, on='issue_id', how='left')
        self.metric_df.loc[:, self.column_name] = self.metric_df.loc[:, self.column_name].fillna(0)
        col_agg_dict = self._consruct_column_names_based_on_agg(self.column_name, self.aggregate_by)
        self.metric_df = self._duplicate_columns(self.metric_df, self.column_name, col_agg_dict.keys())
        self.metric_df = self.metric_df.groupby(self.columns_to_group_by).agg(col_agg_dict).reset_index()
        self.metric_df = self.metric_df.rename(columns={self.column_name + '_mean': self.column_name})
        return self.metric_df
