"""
This module connects to Sharepoint instance with user's credentials from config.yml
"""
import logging

from office365.sharepoint.client_context import ClientContext
from ..utils.read_config import SharePointConfig


def connect_to_sharepoint(config_path: str = "conf/config.yml") -> ClientContext:
    """
    Connect to Sharepoint instance with client's credentials from config.yml
    """
    ctx = None
    try:
        config = SharePointConfig(config_path)
        client_id = config.client_id
        site_url = config.url
        client_secret = config.client_secret

        try:
            ctx = ClientContext(site_url).with_client_credentials(client_id, client_secret)
        except ValueError as err:
            logging.error(f'Could not connect to Sharepoint. {err}')
            raise err

        return ctx

    except KeyError as err:
        logging.error(f'Could not find a key in the {config_path}: {err}')
        raise err
