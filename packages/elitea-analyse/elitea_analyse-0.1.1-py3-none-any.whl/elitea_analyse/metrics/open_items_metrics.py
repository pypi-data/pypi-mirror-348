""" This module contains the OpenItemsMetrics class. """
import logging
from typing_extensions import Self
import pandas as pd

from src.metrics.base_metric import BaseMetric
from src.metrics.life_time import LifeTimeMetric
from src.metrics.items_count import ItemsCountMetric

from src.metrics.constants import OPEN
from src.utils.constants import WAITING_FOR_RELEASE_STATUS
# pylint: disable=attribute-defined-outside-init


class OpenItemsMetrics(BaseMetric):
    """ This class calculates the lead time, cycle time and number of closed items per month. """
    def __init__(self, work_items: pd.DataFrame, basic_columns_to_group_by: list = None,
                 aggregate_by: list = None):
        work_items = work_items.query(f"request_type == '{OPEN}' & status_history != '{WAITING_FOR_RELEASE_STATUS}'")
        super().__init__(work_items, basic_columns_to_group_by, aggregate_by)
        self.columns_to_group_by.append('status')
        self.life_time = self.velocity = None

    def configure_metrics(self, life_time: LifeTimeMetric = None, velocity: ItemsCountMetric = None) -> Self:
        """ Configure metrics for open items. If not provided, metrics will be configured based on class data."""
        self.life_time = life_time or LifeTimeMetric(self.work_items, self.columns_to_group_by, self.aggregate_by)
        self.velocity = velocity or ItemsCountMetric(self.work_items, self.columns_to_group_by)
        return self

    def calculate(self) -> pd.DataFrame:
        """
        Calculate and return the average lifetime, count of open issues grouped by team, project and issue type.
        """
        if (res := super().calculate()) is not None:
            return res

        if not (self.life_time and self.velocity):
            logging.info('Open Items metrics are not configured, calling configure_metrics.')
            self.configure_metrics(self.life_time, self.velocity)

        df_life_time = self.life_time.calculate()
        df_velocity = self.velocity.calculate()

        self.metric_df = df_life_time.merge(df_velocity, on=self.columns_to_group_by, how='outer')

        logging.info('Calculated metrics for open items: number of open items and their Life Time.')
        return self.metric_df
