""" This module contains the VelocityMetric class. """
import pandas as pd

from src.metrics.base_metric import BaseMetric
from src.metrics.constants import ITEMS_COUNT
# pylint: disable=attribute-defined-outside-init


class ItemsCountMetric(BaseMetric):
    """
    This class calculates number of items.
    """
    def calculate(self) -> pd.DataFrame:
        """ Calculate and return the number of items"""
        if (res := super().calculate()) is not None:
            return res

        self.metric_df = self.work_items.drop_duplicates(subset=['issue_id'])\
            .groupby(self.columns_to_group_by).agg({'issue_id': 'count'}).reset_index()
        self.metric_df = self.metric_df.rename(columns={'issue_id': ITEMS_COUNT})
        return self.metric_df
