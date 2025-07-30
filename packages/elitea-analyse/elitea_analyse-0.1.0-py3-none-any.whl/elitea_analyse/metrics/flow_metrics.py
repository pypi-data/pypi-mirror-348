""" This module contains the FlowMetrics class. """
import logging
from typing_extensions import Self
import pandas as pd

from src.metrics.status_based_metric import StatusBasedMetric
from src.metrics.flow_efficiency import FlowEfficiencyMetric
from src.metrics.flow_load import FlowLoadMetric
from src.metrics.lead_time import LeadTimeMetric
from src.metrics.items_count import ItemsCountMetric

from src.metrics.constants import FLOW_VELOCITY, FLOW_TIME, ITEMS_COUNT, YEAR_MONTH, CLOSED
# pylint: disable=attribute-defined-outside-init


class FlowMetrics(StatusBasedMetric):
    """ This class calculates the flow metrics: Flow Load, Flow Time, Flow Velocity and Flow Efficiency. """
    def __init__(self, work_items: pd.DataFrame, statuses_mapping: pd.DataFrame,
                 basic_columns_to_group_by: list = None, aggregate_by: list = None):
        work_items.loc[:, YEAR_MONTH] = work_items['resolved_date'].dt.to_period('M')
        super().__init__(work_items, statuses_mapping, basic_columns_to_group_by, aggregate_by)
        if YEAR_MONTH not in self.columns_to_group_by:
            self.columns_to_group_by.append(YEAR_MONTH)
        self.flow_load = self.flow_efficiency = self.flow_time = self.flow_velocity = None

    def configure_metrics(self, flow_load: FlowLoadMetric = None, flow_efficiency: FlowEfficiencyMetric = None,
                          flow_time: LeadTimeMetric = None, flow_velocity: ItemsCountMetric = None) -> Self:
        """ Configure flow metrics. If not provided, metrics will be configured based on class data."""
        self.flow_load = flow_load or FlowLoadMetric(self.work_items, self.columns_to_group_by)
        closed_work_items = self._filter_items(self.work_items, (self.work_items['request_type'] == CLOSED))
        self.flow_efficiency = flow_efficiency or FlowEfficiencyMetric(closed_work_items, self.statuses_mapping,
                                                                       self.columns_to_group_by, self.aggregate_by)
        self.flow_time = flow_time or LeadTimeMetric(closed_work_items, self.columns_to_group_by, self.aggregate_by)
        self.flow_time.column_name = FLOW_TIME
        self.flow_velocity = flow_velocity or ItemsCountMetric(closed_work_items, self.columns_to_group_by)
        return self

    def calculate(self) -> pd.DataFrame:
        """
        Combine flow metrics to one Dataframe.
        """
        if (res := super().calculate()) is not None:
            return res

        if not (self.flow_load and self.flow_efficiency and self.flow_time and self.flow_velocity):
            logging.info('Flow metrics are not configured, calling configure_metrics.')
            self.configure_metrics(self.flow_load, self.flow_efficiency, self.flow_time, self.flow_velocity)

        df_flow_efficiency = self.flow_efficiency.calculate()
        df_flow_load = self.flow_load.calculate()
        df_flow_time = self.flow_time.calculate()
        df_flow_velocity = self.flow_velocity.calculate().rename(columns={ITEMS_COUNT: FLOW_VELOCITY})

        self.metric_df = df_flow_efficiency.merge(df_flow_load, on=self.columns_to_group_by, how='outer')
        self.metric_df = self.metric_df.merge(df_flow_time, on=self.columns_to_group_by, how='outer')
        self.metric_df = self.metric_df.merge(df_flow_velocity, on=self.columns_to_group_by, how='outer')

        logging.info('Calculated Flow metrics: FLow Load, Flow Time and Flow Velocity.')
        return self.metric_df
