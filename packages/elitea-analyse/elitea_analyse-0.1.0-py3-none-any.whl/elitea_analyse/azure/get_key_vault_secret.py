"""This module gets a secret value from an Azure Key Vault instance."""

import logging

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core import exceptions


def get_secret(vault_url: str, secret_name: str) -> str:
    """Get a secret value from a key vault."""
    key_vault = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    try:
        return key_vault.get_secret(name=secret_name).value
    except exceptions.AzureError as err:
        logging.info(err)
        return None
