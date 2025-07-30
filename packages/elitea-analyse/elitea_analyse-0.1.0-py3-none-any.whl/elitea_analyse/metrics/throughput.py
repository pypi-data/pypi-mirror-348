""" This module contains the ThroughputMetric class. """
from calendar import monthrange
import pandas as pd

from src.metrics.base_metric import BaseMetric
from src.metrics.constants import YEAR_MONTH, CLOSED, THROUGHPUT
# pylint: disable=attribute-defined-outside-init


class ThroughputMetric(BaseMetric):
    """
    This class calculates the Throughput metric.
    """
    def __init__(self, work_items: pd.DataFrame, basic_columns_to_group_by: list = None):
        work_items = self._filter_items(work_items, (work_items['request_type'] == CLOSED))
        super().__init__(work_items, basic_columns_to_group_by)
        if YEAR_MONTH not in self.columns_to_group_by:
            self.columns_to_group_by.append(YEAR_MONTH)

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Throughput as an average number of work items closed per day. The average is calculated per
        calendar month, team, issue type.
        """
        if (res := super().calculate()) is not None:
            return res

        self.work_items.loc[:, YEAR_MONTH] = self.work_items['resolved_date'].dt.to_period('M')
        self.metric_df = self.work_items.drop_duplicates(subset=['issue_id'])\
            .groupby(by=self.columns_to_group_by).agg({'issue_id': 'count'}).reset_index()
        self.metric_df.loc[:, 'days_in_a_month'] = self.metric_df[YEAR_MONTH].apply(
            lambda x: monthrange(x.year, x.month)[1])
        self.metric_df.loc[:, THROUGHPUT] = self.metric_df['issue_id'] / self.metric_df['days_in_a_month']
        self.metric_df = self.metric_df.drop(['issue_id', 'days_in_a_month'], axis=1)
        return self.metric_df
