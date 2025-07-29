from ...utils import logs

# Google Cloud lib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class TokenLoader:
    def __init__(self):
        self._cached_token = None
        self._cached_token_loaded = None
    
    def is_valid_token(self, user_token) -> bool:
        """
        Checks if the current credentials token is valid.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        try:
            return self.load(user_token).valid
        except:
            return False
        
    def load(self, user_token: any) -> Credentials:
        """Converts raw token data to Credentials."""
        if self._cached_token_loaded and self._cached_token == user_token:
            logs.log('Using cached token...', 'info')
            return self._cached_token_loaded
        _cached_token = user_token
        
        try:
            if isinstance(user_token, Credentials):
                logs.log('Loaded token as Credentials object...', 'info')
                
            if isinstance(user_token, str):  # assume it's a path
                logs.log('Loading token as JSON file...', 'info')
                user_token = Credentials.from_authorized_user_file(user_token)
            
            if isinstance(user_token, dict):
                logs.log('Loading token as dict...', 'info')
                user_token = Credentials.from_authorized_user_info(user_token)
                
            if user_token.valid or user_token.expired:
                if user_token.expired:
                    logs.log('Refreshing token...', 'info')
                    user_token.refresh(Request())
                
                logs.log('Token is valid!', 'info')
                logs.log('Token cached.', 'info')
                
                self._set_cache_token(_cached_token, user_token)
                return user_token
            
            if not user_token.valid:
                logs.log('Token is not valid!', 'info')
                return
        except:
            logs.log('Token is not valid!', 'info')
            return
        
    def _set_cache_token(self, cached_token, cached_token_loaded):
        self._cached_token = cached_token
        self._cached_token_loaded = cached_token_loaded
        