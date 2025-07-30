"""This module reads files in an Azure Blob Storage."""

import logging
from io import StringIO
import pandas as pd

from azure.storage.blob import ContainerClient
from azure.core import exceptions


def get_container_client(blob_conn_string: str, container_name: str) -> ContainerClient:
    """Return a container client."""
    container_client = ContainerClient.from_connection_string(conn_str=blob_conn_string,
                                                              container_name=container_name)
    if not container_client.exists():
        raise ValueError(f"Container '{container_name}' doesn't exists!")
    return container_client


def read_blob(blob_conn_string: str, container_name: str, blob_name: str) -> pd.DataFrame:
    """Read data in the blob and return a DataFrame."""
    container_client = get_container_client(blob_conn_string, container_name)

    try:
        blob_client = container_client.get_blob_client(blob=blob_name)
        data = blob_client.download_blob()
        return pd.read_csv(StringIO(data.content_as_text())).drop(columns=['id'])
    except exceptions.AzureError as err:
        logging.exception(err)
        return pd.DataFrame()
