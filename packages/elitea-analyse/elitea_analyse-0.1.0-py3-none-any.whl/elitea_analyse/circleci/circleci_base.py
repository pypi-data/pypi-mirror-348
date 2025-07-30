# pylint: disable='invalid-name'
"""This module contains the class CircleciBase."""

import json
import logging

from json import JSONDecodeError

import requests
import pandas as pd

from requests import RequestException


# pylint: disable='too-few-public-methods'
class CircleciBase:
    """
    A class to interact with the CircleCI API.

    Attributes:
        org_name (str): The organization ID.
        project (str): The project name or ID.
        token (str, optional): The API token. Defaults to None.
        session (requests.Session): The requests Session object for making API requests.

    """
    base_url = 'https://circleci.com/api/v2/'

    def __init__(self, org_name: str, project: str, token: str):
        """
        Constructs all the necessary attributes for the CircleciBase object.

        Args:
            org_name (str): The organization name.
            project (str): The project name.
            token (str, optional): The API token. Defaults to None.
        """
        self.org_name = org_name
        self.token = token
        self.project = project
        self.headers = {
            "Circle-Token": f"{self.token}",
            "Accept": "application/json",
        }
        self.session = requests.Session()

    def get_pipelines_with_workflows(self) -> pd.DataFrame:
        """
        Get pipelines runs merged with workflows details.
        """
        df_pipelines = self._get_all_pipelines()
        if df_pipelines.empty:
            return pd.DataFrame()
        df_workflows = self._get_pipeline_workflows(df_pipelines['pipeline_id'].tolist())
        df_pipelines_with_workflows = df_pipelines.merge(df_workflows, on='pipeline_id')
        logging.info("Extracted pipelines' runs for the project %s with workflows details.", self.project)
        return df_pipelines_with_workflows

    def _get_all_pipelines(self) -> pd.DataFrame:
        """
        Get all pipelines' runs.
        Details on a page:
        https://circleci.com/docs/api/v2/index.html#operation/listPipelinesForProject
        """
        df = self._load_data(f'project/gh/{self.org_name}/{self.project}/pipeline')
        if df.empty:
            return pd.DataFrame()
        df = df.rename(columns={'id': 'pipeline_id', 'created_at': 'pipeline_created_at'})
        logging.info("Extracted pipelines' runs for the project %s", self.project)
        return df

    def _get_pipeline_workflows(self, pipeline_ids: list) -> pd.DataFrame:
        """
        Get workflows details for a pipeline run.
        Details on page:
        https://circleci.com/docs/api/v2/index.html#operation/getWorkflowById
        """
        df = pd.DataFrame()
        for pipeline_id in pipeline_ids:
            df_one_pipeline = self._load_data(f'pipeline/{pipeline_id}/workflow')
            logging.info('Extracted workflows for the pipeline %s.', pipeline_id)
            df = pd.concat([df, df_one_pipeline])
        df = df.drop(columns=['project_slug'])
        df = df.rename(columns={'name': 'workflow'})
        return df

    def _load_data(self, url_suffix: str) -> pd.DataFrame:
        """
        Makes GET request to load data from Circleci API.
        """
        data = []
        next_page = None
        with requests.Session() as session:
            session.headers.update(self.headers)
            while True:
                try:
                    request_url = f"{self.base_url}{url_suffix}"
                    if next_page:
                        request_url += f'?page-token={next_page}'
                    req = session.get(request_url, timeout=10)
                    req.raise_for_status()
                    content = json.loads(req.content)
                    data += content.get('items', [])
                    next_page = content.get('next_page_token')
                    if not next_page:
                        break
                except RequestException as e:
                    logging.warning('An error occurred: %s', e)
                    break
                except JSONDecodeError as e:
                    logging.warning('Failed to parse response content: %s', e)
                    break
        return pd.json_normalize(data)
