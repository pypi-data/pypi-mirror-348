"""
This module to extract data form Click Up platform (spaces, folders, lists, tasks).
"""
import logging
from typing import Optional

import requests

import pandas as pd

from src.utils.convert_to_datetime import unix_milliseconds_to_datetime
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ClickUpGet:
    """
    A class to get data from Click Up.
    Attributes:
        workspace: str
            the id of a Click Up Workspace (Team);
        token: str
            a token, which is needed for the Click Up authorization.
        session: requests.Session()
    """

    def __init__(self, workspace: str, token: str):
        """
        Initialize the class with the workspace and token.
        Args:
            workspace: str
                the id of a Click Up Workspace (Team);
            token: str
                a token, which is needed for the Click Up authorization.
        """
        self.workspace = workspace
        self.token = token
        self.session = requests.Session()

    def get_spaces(self) -> dict:
        """Get all spaces.
        Details on the page: https://clickup.com/api/clickupreference/operation/GetSpaces/
        """
        request_url = f"https://api.clickup.com/api/v2/team/{self.workspace}/space"
        response = self.make_get_request(request_url, headers={"Authorization": self.token},
                                         params={"archived": "False"})
        try:
            data = response.json()['spaces']
        except KeyError as err:
            logger.error('Error while getting spaces: %s', err)
            raise err
        return data

    def get_folders(self, space_id) -> list:
        """Get folders in the specific space.
        Returns information on:
        - id
        - name
        - lists
        Details on the page:https://clickup.com/api/clickupreference/operation/GetFolders/
        """
        request_url = f"https://api.clickup.com/api/v2/space/{space_id}/folder"
        response = self.make_get_request(request_url, headers={"Authorization": self.token},
                                         params={"archived": "False"})
        try:
            data = response.json()['folders']
        except KeyError as err:
            logger.error('Error while getting folders: %s', err)
            raise err
        return data

    @staticmethod
    def get_folders_ids_and_names(folders_info: list) -> list:
        """Extract folders' ids and names fom raw folders' data."""
        try:
            return [{'folder_id': folder['id'], 'folder_name': folder['name']} for folder in folders_info]
        except KeyError as err:
            logger.error('Error while getting folders ids and names: %s', err)
            raise err

    def get_lists_in_folder(self, folder_id) -> dict:
        """Get lists in the specific folder.
        Details on the page:https://clickup.com/api/clickupreference/operation/GetLists/
        """
        request_url = f"https://api.clickup.com/api/v2/folder/{folder_id}/list"
        response = self.make_get_request(request_url, headers={"Authorization": self.token},
                                         params={"archived": "False"})
        try:
            data = response.json()['lists']
        except KeyError as err:
            logger.error('Error while getting lists in folder: %s', err)
            raise err
        return data

    def get_lists_in_root_of_space(self, space_id) -> list:
        """Get lists in the root of the specific spce.
        Details on the page:https://clickup.com/api/clickupreference/operation/GetLists/
        """
        request_url = f"https://api.clickup.com/api/v2/space/{space_id}/list"
        response = self.make_get_request(request_url, headers={"Authorization": self.token},
                                         params={"archived": "False"})
        try:
            data = response.json()['lists']
        except KeyError as err:
            logger.error('Error while getting lists in root of space: %s', err)
            raise err
        return data

    @staticmethod
    def get_spaces_ids_and_names(spaces_info: dict) -> list:
        """Extract spaces' ids and names fom raw folders' data."""
        try:
            return [{'space_id': space['id'], 'space_name': space['name']} for space in spaces_info]
        except KeyError as err:
            logger.error('Error while getting spaces ids and names: %s', err)
            raise err

    def make_get_request(self, request_url: str, **kwargs) -> requests.Response:
        """Make request to an API endpoint."""
        try:
            response = self.session.get(request_url, **kwargs)
        except requests.exceptions.RequestException as err:
            raise SystemExit('Exception occured while sending GET request:', err) from err
        response.raise_for_status()
        return response

    def get_tasks(self, list_id: int, updated_after: int) -> list:
        """Get all tasks in the specific list.
        Details on the page:
        https://clickup.com/api/clickupreference/operation/GetTasks/
        """
        request_url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
        query = {
            "archived": "False",
            "include_markdown_description": "True",
            "page": 0,
            "reverse": "True",
            "subtasks": "True",
            "include_closed": "True",
            "date_updated_gt": updated_after,

        }
        last_page = False
        data = []
        while not last_page:
            response = self.make_get_request(request_url, headers={"Authorization": self.token}, params=query)
            try:
                data_chunk = response.json()['tasks']
                last_page = response.json()['last_page']
                data.extend(data_chunk)
                query['page'] += 1
            except KeyError as err:
                logger.error('Error while getting tasks: %s', err)
                raise err
        return data

    def get_time_in_status(self, task_id: int) -> list:
        """Get task's time in status.
        Details on the page:
        https://clickup.com/api/clickupreference/operation/GetTask'sTimeinStatus/
        """
        request_url = f"https://api.clickup.com/api/v2/task/{task_id}/time_in_status"
        query = {
            "custom_task_ids": "true",
            "team_id": self.workspace,
        }
        response = self.make_get_request(request_url, headers={"Authorization": self.token},
                                         params=query)
        try:
            data = response.json()['status_history']
        except KeyError as err:
            logger.error('Error while getting time in status: %s', err)
            raise err

        return data

    def get_time_in_status_for_all_tasks(self, tasks_ids: list) -> pd.DataFrame:
        """Loop tasks' ids, get time in status data and transform it to the DataFrame."""
        time_in_status_all = []
        for task in tasks_ids:
            time_in_status = self.get_time_in_status(task)
            time_in_status = [{**i, 'issue_id': task} for i in time_in_status]
            time_in_status_all.extend(time_in_status)
        return pd.json_normalize(time_in_status_all, max_level=1)

    def tasks_to_dataframe(self, tasks_dict: list) -> pd.DataFrame:
        """Upload tasks' data (both default and custom parameters) to DataFrame."""
        tasks = []
        for task_raw in tasks_dict:
            task = {}
            task = self.get_task_default_params(task, task_raw)
            task = self.get_tasks_custom_params(task, task_raw)
            tasks.append(task)
        df_tasks = pd.DataFrame.from_records(tasks)
        return df_tasks

    def get_tasks_to_dataframe_for_several_lists(self, updated_after: int, lists_ids: list) -> Optional[pd.DataFrame]:
        """Get tasks from several Click Up Lists."""
        df_tasks = pd.DataFrame()
        for lst in lists_ids:
            tasks_lst = self.get_tasks(lst, updated_after)
            if tasks_lst:
                df_tasks_chunk = self.tasks_to_dataframe(tasks_lst)
                df_tasks = pd.concat([df_tasks, df_tasks_chunk], ignore_index=True)
        return df_tasks

    @staticmethod
    def get_task_default_params(task: dict, task_raw: dict) -> dict:
        """Get values of a task default parameters."""
        task['issue_key'] = task_raw['custom_id']
        task['issue_id'] = task_raw['id']

        priority = task_raw.get('priority')
        if priority:
            task['priority'] = priority.get('priority')

        task['summary'] = task_raw['name']
        task['status'] = task_raw['status'].get('status')
        task['linked_issues'] = task_raw['linked_tasks']
        task['subtasks'] = task_raw.get('subtasks')

        task['created_date'] = unix_milliseconds_to_datetime(task_raw.get('date_created'))
        task['resolved_date'] = unix_milliseconds_to_datetime(task_raw.get('date_done'))
        task['closed_date'] = unix_milliseconds_to_datetime(task_raw.get('date_closed'))
        task['last_updated_date'] = unix_milliseconds_to_datetime(task_raw.get('date_updated'))

        task['project_name'] = task_raw['project'].get('name')  # get from spaces list
        task['total_time_spent'] = task_raw.get('time_spent')
        task['space_id'] = task_raw['space'].get('id')
        task['space_name'] = task_raw['space'].get('id')
        task['list_id'] = task_raw['list'].get('id')
        task['folder_id'] = task_raw['folder'].get('id')

        return task

    @staticmethod
    def get_tasks_custom_params(task: dict, task_raw: dict) -> dict:
        """Get values of a task custom parameters."""
        custom_fields = task_raw.get('custom_fields')

        for key, value in {'issue_type': 'Type',
                           'team': 'Department/Team',
                           'fix_versions': 'Version',
                           'product': 'Product',
                           'product_manager': 'Product Manager'}.items():
            task[key] = None
            try:
                custom_field = list(filter(lambda d, v=value: d['name'] == v, custom_fields))[0]
                task[key] = custom_field.get('value')
            except IndexError as err:
                logger.warning('Exception occured while getting custom fields: %s', err)

        if task['product_manager']:
            task['product_manager'] = ';'.join([manager.get('username') for manager in task['product_manager']])
        return task

    def get_lists_from_folders_data(self, folders: list) -> list:
        """Get lists that are in folders."""
        lists_in_folders = []
        for folder in folders:
            lists_ids_one_folder = [lst for lst in folder.get('lists') if folder.get('lists')]
            lists_ids_one_folder = [
                self.add_space_and_folder_data_to_list(lst, folder, 'folder') for lst in lists_ids_one_folder]
            lists_in_folders.extend(lists_ids_one_folder)
        return lists_in_folders

    @staticmethod
    def add_space_and_folder_data_to_list(lst_data: dict, input_data: dict, folder_or_list: str) -> Optional[dict]:
        """Add information on space id and name, folder id and name to each Click Up list or folder data."""
        if folder_or_list not in ('list', 'folder'):
            raise ValueError("Define Click Up entity to add it's data to the list data.")
        lst_data = lst_data | {'space_id': input_data['space']['id'],
                               'space_name': input_data['space']['name']}
        if folder_or_list == 'folder':
            return lst_data | {'folder_id': input_data['id'],
                               'folder_name': input_data['name']}
        return lst_data | {'folder_id': input_data['folder']['id'],
                           'folder_name': input_data['folder']['name']}

    def get_all_lists(self, lists_in_folders: list, lists_in_space: list) -> pd.DataFrame:
        """Get all lists, both which in folders and in the root of a space."""
        lists_in_space = [lst for lst in lists_in_space if lst.get('archived') is False]
        lists_in_space = [self.add_space_and_folder_data_to_list(lst, lst, "list") for lst in lists_in_space]
        lists_all = lists_in_folders + lists_in_space
        return pd.DataFrame.from_records(lists_all)[
            ['id', 'name', 'space_id', 'space_name', 'folder_id', 'folder_name']].rename(
            columns={'id': 'list_id', 'name': 'list_name'})

    def get_custom_fields(self, space_id: int):
        """Get Custom Fields available on tasks in a specific List.
        Details on the page:https://clickup.com/api/clickupreference/operation/GetAccessibleCustomFields/
        """
        request_url = f"https://api.clickup.com/api/v2/list/{space_id}/field"
        response = self.make_get_request(request_url, headers={"Authorization": self.token},
                                         params={"archived": "True"})
        try:
            data = response.json()
        except KeyError as err:
            logger.error('Error while getting custom fields: %s', err)
            raise err
        return data

    def get_tasks_types_mapping(self, lists_ids: list) -> pd.DataFrame:
        """
        Get tasks' order indexes and names for the dropdown lists for the tasks' type in Click Up
        (work s only for Viral Nation).
        """
        custom_fields_all_list = []
        for list_id in lists_ids:
            custom_fields_list = self.get_custom_fields(list_id)['fields']
            try:
                type_field = [custom_field for custom_field in custom_fields_list if custom_field['name'] == 'Type'][0]
                type_config = type_field.get('type_config')
                if type_config:
                    type_options = type_config.get('options')
                    type_options = [dict(option, **{'list_id': list_id}) for option in type_options]
                    custom_fields_all_list = custom_fields_all_list + type_options
            except IndexError as err:
                logger.warning('Exception occured while getting tasks types mapping: %s', err)

        df_type_field = pd.DataFrame.from_records(custom_fields_all_list)
        df_type_field = df_type_field.drop_duplicates(subset=['id', 'name', 'orderindex']).drop(
            columns=['id', 'color', 'list_id'])
        return df_type_field

    @staticmethod
    def get_statuses_order(folders: list) -> pd.DataFrame:
        """Get a DtaFrame with tasks' statuses order i na given ClickUp folders."""
        df_statuses = pd.DataFrame()
        for folder in folders:
            statuses_list = folder.get('statuses')
            if statuses_list:
                df_statuses = pd.concat([df_statuses, pd.DataFrame.from_records(statuses_list)])
        df_statuses = df_statuses.drop_duplicates(subset='status')
        df_statuses = df_statuses.rename(columns={'status': 'status_raw', 'orderindex': 'status_index'})
        return df_statuses[['status_raw', 'status_index']]
