"""This module is an entry point to extract data from Click Up."""

import logging
from datetime import datetime
from typing import Optional

import pandas as pd

from clickup_transform import ClickUpTransform
from clickup import ClickUpGet
from src.utils.read_config import ClickUpConfig
from src.utils.convert_to_datetime import string_to_unix_milliseconds

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DATA_EXTRACTION_DATE = datetime.utcnow()


def get_tasks_from_one_space(space_id: int, updated_after: str) -> Optional[tuple[
        pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
    """
    Extract data from ClickUp one space: Tasks, Lists, Statuses order, Tasks Types possible values.

    Args:
        space_id (int): The ID of the space to extract data from.
        updated_after (str): The date and time to filter tasks by. Only tasks updated after this date will be extracted.

    Returns:
        Optional[tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]]:
        A tuple containing the extracted dataframes for Tasks, Statuses, Tasks Types, and Lists respectively.
        Returns None if no data is found.
    """
    updated_after = string_to_unix_milliseconds(updated_after)
    conf_clickup = ClickUpConfig('../../conf/config.yml')
    click_up = ClickUpGet(conf_clickup.workspace_id, conf_clickup.token)
    folders = click_up.get_folders(space_id)
    lists_in_folders = click_up.get_lists_from_folders_data(folders)
    lists_in_space = click_up.get_lists_in_root_of_space(space_id)  # 54345732 VN Tech - MASTER
    df_lists = click_up.get_all_lists(lists_in_folders, lists_in_space)
    if df_lists.empty:
        logger.info('There is no Lists in the space %s', space_id)
        return None

    lists_ids = df_lists['list_id'].tolist()

    # Get tasks to data frame
    df_tasks = click_up.get_tasks_to_dataframe_for_several_lists(updated_after, lists_ids)
    df_tasks['data_extraction_date'] = DATA_EXTRACTION_DATE
    if df_tasks.empty:
        logger.info('There is no Tasks in the space %s', space_id)
        return None

    # Get time in status
    tasks_ids = df_tasks['issue_id'].tolist()
    df_time_in_status = click_up.get_time_in_status_for_all_tasks(tasks_ids)

    df_tasks = ClickUpTransform(df_tasks, df_time_in_status).transform_data(DATA_EXTRACTION_DATE)
    df_statuses = click_up.get_statuses_order(folders)
    logger.info('Data on %s has been extracted.', len(tasks_ids))

    # Get Tasks' types
    df_type_field = click_up.get_tasks_types_mapping(lists_ids)

    return df_tasks, df_statuses, df_type_field, df_lists
