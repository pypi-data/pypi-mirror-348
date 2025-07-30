""" This module contains the StatusBasedMetric class which is a base class for all status based metrics. """
from abc import ABC, abstractmethod
import logging
import pandas as pd

from src.metrics.base_metric import BaseMetric
from src.metrics.constants import CLOSED
# pylint: disable=attribute-defined-outside-init


class StatusBasedMetric(BaseMetric, ABC):
    """
    This is an abstract class that should be inherited by all classes that calculate metrics based on statuses.
    Every inherited class should implement the calculate method that calculates the metric.
    """
    mapping_columns_to_check = {
        'status_raw', 'status_raw_index', 'status_mapped', 'status_mapped_index', 'status_type', 'add_to_cycle_time'}

    def __init__(self, work_items: pd.DataFrame, statuses_mapping: pd.DataFrame,
                 basic_columns_to_group_by: list = None, aggregate_by: list = None):
        super().__init__(work_items, basic_columns_to_group_by, aggregate_by)
        self.statuses_mapping = statuses_mapping
        self._check_input_statuses_mapping()

    @abstractmethod
    def calculate(self) -> pd.DataFrame:
        """
        Calculate and return the metric based on statuses. T
        his method should be implemented in the inherited class.
        """
        if (res := super().calculate()) is not None:
            return res

        if self.statuses_mapping.empty:
            logging.info('There is no statuses mapped for the metrics calculation.')
            return self.metric_df

        return None

    def _check_input_statuses_mapping(self):
        """
        Check if the input dataframe with statuses' mapping contains all the necessary columns, if all the values
        in the columns status_type and add_to_cycle_time are not empty, and if all the statuses has been mapped.
        """
        if self.statuses_mapping.empty:
            return
        self._check_statuses_mapping_columns()
        self._check_if_empty_in_statuses_mapping()
        self._check_if_all_statuses_mapped()

    def _check_statuses_mapping_columns(self):
        """Check if the input dataframe with statuses' mapping contains all the necessary columns."""
        check_list, input_list = self.mapping_columns_to_check, set(self.statuses_mapping.columns)
        if not check_list.issubset(input_list):
            raise KeyError(f'The columns {check_list.difference(input_list)} are missing in the statuses mapping!')

    def _check_if_empty_in_statuses_mapping(self):
        """
        Check if there is no empty values in the input dataframe with statuses' mapping (columns status_type and
        add_to_cycle_time).
        """
        status_type_check_nan = self.statuses_mapping['status_type'].isnull().values.any()
        add_to_cycle_type_check_nan = self.statuses_mapping['add_to_cycle_time'].isnull().values.any()
        if all((status_type_check_nan, add_to_cycle_type_check_nan)):
            raise ValueError('The columns "status_type" and "add_to_cycle_time" should not contain empty values!')
        if status_type_check_nan:
            raise ValueError('The column "status_type" should not contain empty values!')
        if add_to_cycle_type_check_nan:
            raise ValueError('The column "add_to_cycle_type" should not contain empty values!')

    def _check_if_all_statuses_mapped(self):
        """
        Check if all the statuses has been mapped in the input dataframe with statuses' mapping.
        """
        check_list = set(self.work_items[self.work_items['request_type'] == CLOSED]['status_history'].unique())
        input_list = set(self.statuses_mapping['status_raw'])
        if not check_list.issubset(input_list):
            diff = check_list.difference(input_list)
            raise ValueError(f'{diff} status is not in the statuses mapping!')
