"""
This module is designed far calling it functions from the main_git.ipynb.
Functions are used for downloading data from GitLab.
"""
import pandas as pd

from ..git.git_search import GitLabV4Search, GitLabV4
from ..utils.constants import OUTPUT_FOLDER
from ..utils.read_config import GitConfig
from ..utils.check_input import check_if_open
from ..utils.timer import timer


CONFIG_PATH = './conf/config.yml'
GIT_CREDS = GitConfig(CONFIG_PATH)
URL, TOKEN = GIT_CREDS.url, GIT_CREDS.token


@timer
def get_git_projects_list(date: str) -> None:
    """Get projects' list that a user have access to in GitLab."""
    git = GitLabV4Search(url=URL, default_branch_name='master', token=TOKEN)
    git_projects_list_output = f'{OUTPUT_FOLDER}gitlab_projects_info.csv'
    check_if_open(git_projects_list_output)
    result = git.projects_info(date)
    result.to_csv(git_projects_list_output, index=False)
    print(f'You have access to {len(result)}. Data has been downloaded to the folder {OUTPUT_FOLDER}')


@timer
def get_git_projects_info(date: str) -> None:
    """Get extended info on projects that a user have access to in GitLab."""
    git = GitLabV4Search(url=URL, default_branch_name='master', token=TOKEN)
    git_projects_info_output = f'{OUTPUT_FOLDER}gitlab_projects_info_extended.csv'
    check_if_open(git_projects_info_output)
    result = git.extended_project_info(date)
    result.to_csv(git_projects_info_output, index=False)
    print(f'Data has been downloaded to the folder {OUTPUT_FOLDER}')


@timer
def get_git_projects_that_in_jira(project_keys: str) -> None:
    """Get GitLab projects' list by the Jira projects' keys."""
    git = GitLabV4Search(url=URL, default_branch_name='master', token=TOKEN)
    git_projects_that_in_jira = f'{OUTPUT_FOLDER}gitlab_projects_that_in_Jira.csv'
    check_if_open(git_projects_that_in_jira)
    result = git.compile_search(project_keys)
    if isinstance(result, pd.DataFrame) and len(result) != 0:
        result.to_csv(git_projects_that_in_jira, index=False)
        print(f'Data has been downloaded to the folder {OUTPUT_FOLDER}')
        print(result.iloc[:, :2])


@timer
def get_git_commits(project: str, since_date: str) -> None:
    """Get commits' data for one GitLab project."""
    git = GitLabV4(url=URL, project_id=project, default_branch_name='master', token=TOKEN)
    git_commits_output = f'{OUTPUT_FOLDER}commits_details_{project}.csv'
    check_if_open(git_commits_output)
    result = git.get_commits_details_and_size(since_date)
    if isinstance(result, pd.DataFrame) and len(result) != 0:
        result.to_csv(git_commits_output)
    else:
        print(f'There are no commits in the project {project} created after {since_date}')


@timer
def get_git_merge_requests(project: str, since_date: str) -> None:
    """Get merge requests' data for one GitLab project."""
    git = GitLabV4(url=URL, project_id=project, default_branch_name='master', token=TOKEN)
    git_merge_requests_output = f'{OUTPUT_FOLDER}merge_requests_details_{project}.csv'
    check_if_open(git_merge_requests_output)
    result = git.get_all_merge_requests_details(since_date)
    if isinstance(result, pd.DataFrame) and len(result) != 0:
        result.to_csv(git_merge_requests_output)
    else:
        print(f'There are no merge requests in the project {project} created after {since_date}')
