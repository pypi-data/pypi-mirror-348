""" This module contains the ClosedItemsMetrics class. """
import logging
from typing_extensions import Self
import pandas as pd

from src.metrics.status_based_metric import StatusBasedMetric
from src.metrics.lead_time import LeadTimeMetric
from src.metrics.cycle_time import CycleTimeMetric
from src.metrics.items_count import ItemsCountMetric

from src.metrics.constants import CLOSED, YEAR_MONTH
from src.utils.constants import WAITING_FOR_RELEASE_STATUS
# pylint: disable=attribute-defined-outside-init


class ClosedItemsMetrics(StatusBasedMetric):
    """ This class calculates the lead time, cycle time and number of closed items per month. """
    def __init__(self, work_items: pd.DataFrame, statuses_mapping: pd.DataFrame,
                 basic_columns_to_group_by: list = None, aggregate_by: list = None):
        work_items = self._filter_items(work_items, (work_items['request_type'] == CLOSED))\
            .query(f"status_history != '{WAITING_FOR_RELEASE_STATUS}'")
        work_items.loc[:, YEAR_MONTH] = work_items['resolved_date'].dt.to_period('M')
        super().__init__(work_items, statuses_mapping, basic_columns_to_group_by, aggregate_by)

        if YEAR_MONTH not in self.columns_to_group_by:
            self.columns_to_group_by.append(YEAR_MONTH)
        self.lead_time = self.cycle_time = self.velocity = None

    def configure_metrics(self, lead_time: LeadTimeMetric = None, cycle_time: CycleTimeMetric = None,
                          velocity: ItemsCountMetric = None) -> Self:
        """ Configure metrics for closed items. If not provided, metrics will be configured based on class data."""
        self.lead_time = lead_time or LeadTimeMetric(self.work_items, self.columns_to_group_by, self.aggregate_by)
        self.cycle_time = cycle_time or CycleTimeMetric(self.work_items, self.statuses_mapping,
                                                        self.columns_to_group_by, self.aggregate_by)
        self.velocity = velocity or ItemsCountMetric(self.work_items, self.columns_to_group_by)
        return self

    def calculate(self) -> pd.DataFrame:
        """
        Calculate and return the average lead time, cycle time and count of closed issues
        grouped by columns_to_group_by for each month.
        """
        if (res := super().calculate()) is not None:
            return res

        if not (self.lead_time and self.cycle_time and self.velocity):
            logging.info('Closed Items metrics are not configured, calling configure_metrics.')
            self.configure_metrics(self.lead_time, self.cycle_time, self.velocity)

        df_lead_time = self.lead_time.calculate()
        df_cycle_time = self.cycle_time.calculate()
        df_velocity = self.velocity.calculate()

        self.metric_df = df_lead_time.merge(df_cycle_time, on=self.columns_to_group_by, how='outer')
        self.metric_df = self.metric_df.merge(df_velocity, on=self.columns_to_group_by, how='outer')

        logging.info('Calculated Lead Time, Cycle Time and number of closed items per month.')
        return self.metric_df
