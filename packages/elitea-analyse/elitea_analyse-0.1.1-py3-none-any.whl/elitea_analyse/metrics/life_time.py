""" This module contains the LifeTimeMetric class. """
import pandas as pd

from src.metrics.base_metric import BaseMetric
from src.metrics.constants import LIFE_TIME, OPEN
from src.utils.constants import WAITING_FOR_RELEASE_STATUS
# pylint: disable=attribute-defined-outside-init


class LifeTimeMetric(BaseMetric):
    """
    This class calculates the life time metric.
    """
    def __init__(self, work_items: pd.DataFrame, basic_columns_to_group_by: list = None,
                 aggregate_by: list = None):
        work_items = work_items.query(
            f"request_type == '{OPEN}' & status_history != '{WAITING_FOR_RELEASE_STATUS}'")
        self.column_name = LIFE_TIME
        super().__init__(work_items, basic_columns_to_group_by, aggregate_by)

    def calculate(self) -> pd.DataFrame:
        """
        Calculate and return the lifetime for the given items based on the statuses transition data.
        """
        if (res := super().calculate()) is not None:
            return res

        self.metric_df = self.work_items.pivot_table(index='issue_id', values='time_in_status', aggfunc='sum')
        self.metric_df = self.metric_df.reset_index().rename(columns={'time_in_status': self.column_name})
        self.metric_df = self.work_items.drop_duplicates(subset=['issue_id'])\
            .merge(self.metric_df, on='issue_id', how='left')
        col_agg_dict = self._consruct_column_names_based_on_agg(self.column_name, self.aggregate_by)
        self.metric_df = self._duplicate_columns(self.metric_df, self.column_name, col_agg_dict.keys())
        self.metric_df = self.metric_df.groupby(self.columns_to_group_by).agg(col_agg_dict).reset_index()
        self.metric_df = self.metric_df.rename(columns={self.column_name + '_mean': self.column_name})
        return self.metric_df
