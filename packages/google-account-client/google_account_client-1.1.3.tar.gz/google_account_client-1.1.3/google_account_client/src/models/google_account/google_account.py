"""
google_account.py

Defines the GoogleAccount class, a high-level interface that consolidates Google Calendar
functionality and Google API authentication/authorization handling. It inherits behavior
from service and calendar mixins, and provides scoped, logged access to Google APIs
with user-specific credentials.
"""

from .google_service import GoogleServiceCredentials
from .google_calendar import GoogleCalendar

# Google Cloud lib
from google.oauth2.service_account import Credentials

class GoogleAccount(GoogleServiceCredentials, GoogleCalendar):
    """
    GoogleAccount is the main interface for managing a user's Google Calendar and 
    authentication credentials.

    Inherits from:
        - GoogleServiceCredentials: Handles credential loading and refreshing.
        - GoogleCalendar: Provides calendar-related methods (listing, creating events, etc.).
    """
    def __init__(self, name: str, user_token: any = None, credentials: Credentials = None):
        """
        Initializes a new GoogleAccount instance.

        Args:
            name (str): User or account identifier.
            user_token (any): Existing credentials object (optional).
            credentials (any): Raw credential information or dict (optional).
            logger (any): Logger instance (optional).
        """
        # Personal Info
        self.name = name
        
        # Validate and use user_token
        GoogleServiceCredentials.__init__(self, user_token, credentials)
        
    def __repr__(self):
        return f"<GoogleAccount name='{self.name}'>"