""" This module contains the QueueMetrics class. """
import logging
from typing_extensions import Self
import pandas as pd

from src.metrics.status_based_metric import StatusBasedMetric
from src.metrics.lead_time import LeadTimeMetric
from src.metrics.throughput import ThroughputMetric

from src.metrics.constants import CLOSED, YEAR_MONTH, LEAD_TIME, WIP, THROUGHPUT
from src.utils.constants import WAITING_FOR_RELEASE_STATUS
# pylint: disable=attribute-defined-outside-init


class QueueMetrics(StatusBasedMetric):
    """ This class calculates Throughput, Lead Time and Work In Progress (WIP). """
    def __init__(self, work_items: pd.DataFrame, statuses_mapping: pd.DataFrame,
                 basic_columns_to_group_by: list = None, aggregate_by: list = None):
        work_items = self._filter_items(work_items, (work_items['request_type'] == CLOSED))\
            .query(f"status_history != '{WAITING_FOR_RELEASE_STATUS}'")
        work_items.loc[:, YEAR_MONTH] = work_items['resolved_date'].dt.to_period('M')
        super().__init__(work_items, statuses_mapping, basic_columns_to_group_by, aggregate_by)

        if YEAR_MONTH not in self.columns_to_group_by:
            self.columns_to_group_by.append(YEAR_MONTH)
        self.lead_time = self.throughput = None

    def configure_metrics(self, lead_time: LeadTimeMetric = None, throughput: ThroughputMetric = None) -> Self:
        """ Configure queue metrics. If not provided, metrics will be configured based on class data."""
        self.lead_time = lead_time or LeadTimeMetric(self.work_items, self.columns_to_group_by, self.aggregate_by)
        self.throughput = throughput or ThroughputMetric(self.work_items, self.columns_to_group_by)
        return self

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Throughput, Lead Time and Work In Progress (WIP) per calendar month, project, team, issue type.
        """
        if (res := super().calculate()) is not None:
            return res

        if not (self.lead_time and self.throughput):
            logging.info('Queue metrics are not configured, calling configure_metrics.')
            self.configure_metrics(self.lead_time, self.throughput)

        df_lead_time = self.lead_time.calculate()
        df_throughput = self.throughput.calculate()

        self.metric_df = df_lead_time.merge(df_throughput, on=self.columns_to_group_by, how='outer')
        self.metric_df[WIP] = self.metric_df[THROUGHPUT] * self.metric_df[LEAD_TIME]

        logging.info('Calculated Throughput, Lead Time and WIP.')
        return self.metric_df
