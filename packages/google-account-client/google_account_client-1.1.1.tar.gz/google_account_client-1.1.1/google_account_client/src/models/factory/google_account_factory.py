from ..google_account.google_account import GoogleAccount
from ..auxiliar import logger
from ...settings import Config

import os

class GoogleAccountFactory():
    def __init__(self, client_secrets: str, port: int = None, enable_logs: bool = None):
        """
        Factory to create GoogleAccount instances using a shared client secret (OAuth client).

        Args:
            client_secrets_path (str): Path to the OAuth client secrets JSON file.
            logging (int): Port for the local server flow to listen on.
            enable_logs (bool): If True, enables debug/info logging.
        """
        self.name = 'GoogleAccountFactory'
        self._client_secrets = client_secrets
        
        configs = {
            'port': port,
            'enable_logs': enable_logs
        }
        Config.update_configs(configs)

        if not os.path.exists(client_secrets):
            raise FileNotFoundError(f'Client secret file not found: {client_secrets}')

    def create_account(self, name: str, token: any = None) -> GoogleAccount:
        """
        Creates a new GoogleAccount instance with valid credentials.

        Args:
            name (str): Account identifier.
            token (str | dict | Credentials, optional): Path, dict or Credentials instance for the user token.

        Returns:
            GoogleAccount
        """

        return GoogleAccount(
            name=name,
            user_token=token,
            credentials=self._client_secrets,
        )