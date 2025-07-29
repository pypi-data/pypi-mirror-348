from ...settings import Packages, Config
from .google_interface import GoogleInterface
from ...utils.token_validator_wrapper import ensure_valid_token

# Google Cloud lib
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import json

class GoogleServiceCredentials(GoogleInterface):
    """
    Handles loading and refreshing Google API credentials, and building a service client.

    This class provides utility methods for working with Google API credentials in-memory.
    It avoids writing credentials to disk, and supports automatic refresh or OAuth login
    via the local server flow when needed.

    Methods:
        _load_token(token: any = None) -> any:
            Loads valid credentials, refreshing them if expired, or performing OAuth login if absent.
        
        _load_service(creds: any) -> any:
            Builds and returns a Google Calendar service client using the provided credentials.
    """
    def __init__(self, user_token: any = None, credentials: Credentials = None):
        # Packages
        self.SCOPES = Packages.SCOPES

        # Google-Service-Credentials
        self._user_token = self._load_token(user_token, credentials)
        self._service = self._load_service(self._user_token)
    
    def get_user_token(self) -> any:
        """
        Returns the current credentials token for the account.

        Returns:
            Any: The stored OAuth credentials.
        """
        return self._user_token
    
    def _load_token(self, user_token: any, credentials: Credentials = None) -> Credentials:
        """Converts raw token data to Credentials."""
        if isinstance(user_token, str):  # assume it's a path
            self.log('Extracting token from JSON file...', 'info')
            with open(user_token, 'r') as f:
                user_token = json.load(f)
        
        if isinstance(user_token, dict):
            self.log('Loading token...', 'info')
            return Credentials.from_authorized_user_info(user_token)
        
        if isinstance(user_token, Credentials):
            self.log('Loading token...', 'info')
            return user_token
        
        # No token? Prompt login
        self.log('No token provided, starting OAuth flow.', 'info')
        flow = InstalledAppFlow.from_client_secrets_file(credentials, scopes=['https://www.googleapis.com/auth/calendar'])
        return flow.run_local_server(port=3002, host="0.0.0.0", open_browser=False)

    @ensure_valid_token
    def _load_service(self, user_token: any) -> any:
        """
        Build and return a Google Calendar service client using the given credentials.

        Args:
            token (any): A valid Google credentials object.

        Returns:
            any: A service object to interact with the Google Calendar API.
        """
        return build('calendar', 'v3', credentials=user_token)