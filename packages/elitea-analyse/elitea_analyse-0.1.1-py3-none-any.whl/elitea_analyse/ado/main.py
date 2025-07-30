"""
This module is designed far calling its functions from main_ado.ipynb
Functions are used for downloading data for several projects in Azure DevOps
"""
import pandas as pd

from ..ado.azure_commit import AzureDevOpsCommit
from ..utils.read_config import AdoConfig
from ..utils.check_input import check_if_open
from ..utils.timer import timer
from ..ado.azure import AzureDevOps
from ..utils.constants import OUTPUT_FOLDER, OUTPUT_WORK_ITEMS, OUTPUT_MAPPING


CONFIG_PATH = './conf/config.yml'
ADO_CREDS = AdoConfig(CONFIG_PATH)
ORGANIZATION, USER, TOKEN = ADO_CREDS.organization, ADO_CREDS.user, ADO_CREDS.token


# Get information on work items
@timer
def get_work_items_several_projects(projects, resolved_after, updated_after, created_after, area):
    """Get work items of several projects."""
    projects_list = projects.split(',')
    df_result = pd.DataFrame()
    for project in projects_list:
        ads = AzureDevOps(ORGANIZATION, project, 'main', USER, token=TOKEN)
        df_wi_history, df_statuses = ads.concat_work_items_and_history(
            resolved_after, updated_after, created_after, area)
        if df_statuses is not None:
            file_statuses = f'{OUTPUT_MAPPING}{project}.csv'
            check_if_open(file_statuses)
            df_statuses.to_csv(file_statuses, index=True, index_label='id')
            df_result = pd.concat([df_result, df_wi_history], axis=0)
    file_result = f'{OUTPUT_WORK_ITEMS}{projects}.csv'
    check_if_open(file_result)
    df_result.to_csv(file_result, index=True, index_label='id')
    return df_result


async def get_commits_several_projects(project, since_date, new_version=True, with_commit_size=True):
    """Get ADO commits of several projects."""
    # transform projects names to list
    projects_lst = project.replace(' ', '').split(',')
    # check if csv files with the same name are open
    f1 = f'{OUTPUT_FOLDER}commits_details_{project}.csv'
    check_if_open(f1)
    result_df = pd.DataFrame()
    # loop through projects
    for prj in projects_lst:
        ads = AzureDevOpsCommit(ORGANIZATION, prj, USER, token=TOKEN)
        if new_version:
            df1 = await ads.get_commits_details(since_date, with_commit_size)
        else:
            df1 = await ads.get_commits_details_and_size(since_date)
        if df1 is None:
            print(f'There are no comments for the selected period in {prj} project!')
            continue
        result_df = pd.concat([result_df, df1], axis=0)
    result_df.to_csv(f1, index=False)
    print('Commits have been extracted')
    return result_df


def get_merge_requests_several_projects(project, since_date):
    """Get ADO merge requests of several projects."""
    # transform projects names to list
    projects_lst = project.split(',')
    # check if csv files with the same name are open
    f2 = f'{OUTPUT_FOLDER}merge_requests_details_{project}.csv'
    check_if_open(f2)
    result_df = pd.DataFrame()
    # loop through projects
    for prj in projects_lst:
        ads = AzureDevOps(ORGANIZATION, prj, 'main', USER, token=TOKEN)
        df1 = ads.get_all_pull_requests_details(since_date)
        if df1 is not None:
            result_df = pd.concat([result_df, df1], axis=0)
    result_df.to_csv(f2, index=False)
    return result_df


def get_pipelines_runs_several_projects(project):
    """Get ADO pipelines runs of several projects."""
    # transform projects names to list
    projects_lst = project.split(',')
    # check if csv files with the same name are open
    f = f'{OUTPUT_FOLDER}pipelines_runs_{project}.csv'
    check_if_open(f)
    result_df = pd.DataFrame()
    # loop through projects
    for prj in projects_lst:
        ads = AzureDevOps(ORGANIZATION, prj, 'main', USER, token=TOKEN)
        df1 = ads.get_pipelines_runs_and_timeline()
        if df1 is not None:
            result_df = pd.concat([result_df, df1], axis=0)
    result_df.to_csv(f, index=False)
    return result_df
