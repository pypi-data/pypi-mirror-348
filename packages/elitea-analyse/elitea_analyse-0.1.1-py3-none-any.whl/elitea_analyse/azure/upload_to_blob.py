"""This module uplods files to an Azure Blob Storage."""
import logging

from azure.core import exceptions

from src.azure.read_blob import get_container_client


def upload_to_blob(blob_conn_string: str, container_name: str, blob_name: str, data_to_upload) -> None:
    """Upload data to blob and replace existing files there."""
    container_client = get_container_client(blob_conn_string, container_name)

    try:
        container_client.upload_blob(name=blob_name,
                                     data=data_to_upload,
                                     overwrite=True,
                                     blob_type='BlockBlob')
    except exceptions.AzureError as err:
        logging.info(err)
