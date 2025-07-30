""" A module to represent Sharepoint instance to read and write files. """
import io
import logging
from typing import Optional

import pandas as pd

from office365.sharepoint.files.file import File
from office365.sharepoint.files.file import Folder
from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request_exception import ClientRequestException


class SharePoint:
    """
    A class to represent Sharepoint instance to read and write files.
    Attributes:
        ctx: ClientContext
            a connection to the Sharepoint instance.
        site: str
            a name of the Sharepoint site.
    """

    def __init__(self, ctx: ClientContext, site: str):
        self.site = site
        self.ctx = ctx
        self.base_path = f"/sites/{site}/Shared Documents/"

    def try_get_file(self, url: str) -> Optional[File]:
        """
        Checks if folder exists by attempting to open it.
        """
        try:
            return self.ctx.web.get_file_by_server_relative_path(url).get().execute_query()
        except ClientRequestException as e:
            if e.response.status_code >= 400:
                logging.error(f"Error reading file {url}: {e.response.status_code}")
            raise e

    def try_get_folder(self, url: str) -> Optional[Folder]:
        """
        Checks if folder exists by attempting to open it.
        """
        try:
            return self.ctx.web.get_folder_by_server_relative_path(url).get().execute_query()
        except ClientRequestException as e:
            if e.response.status_code >= 400:
                logging.error(f"Error reading folder {url}: {e.response.status_code}")
            raise e

    def create_directory(self, dir_name: str) -> None:
        """
        Creates a folder in the sharepoint directory.
        """
        if dir_name:
            result = self.ctx.web.folders.add(f'Shared Documents/{dir_name}').execute_query()
            if result:
                logging.info(f"Folder created: 'Shared Documents/{dir_name}'")
            else:
                raise ValueError(f"Folder creation failed: 'Shared Documents/{dir_name}'")
        else:
            logging.error("Folder name is empty. No folder created.")

    def write_dataframe_to_csv(self, folder: str, file_name: str, df: pd.DataFrame) -> None:
        """
        Writes a file to the sharepoint directory.
        """
        try:
            target_folder = self.ctx.web.get_folder_by_server_relative_url(f"{self.base_path}{folder}")
            buffer = io.BytesIO()
            df.to_csv(buffer, index_label='id')
            buffer.seek(0)
            file_content = buffer.read()
            target_folder.upload_file(file_name, file_content).execute_query()
        except OSError as e:
            logging.error(f"Upload failed. File: '{file_name}' upload to: '{self.base_path}{folder}'")
            raise e

        logging.info(f"Upload successful. File: '{file_name}'  uploaded to: '{self.base_path}{folder}'")

    def read_dataframe_from_csv(self, folder: str, file_name: str) -> pd.DataFrame:
        """
        Reads a file from the sharepoint directory.
        """
        df = pd.DataFrame()

        file_full_path = self.base_path + folder + "/" + file_name

        if self.try_get_file(file_full_path) is None:
            logging.error(f"File: '{file_name}' on path: '{file_full_path}' does not exists.")
            return df

        response = File.open_binary(self.ctx, file_full_path)
        df = pd.read_csv(io.BytesIO(response.content))

        return df
