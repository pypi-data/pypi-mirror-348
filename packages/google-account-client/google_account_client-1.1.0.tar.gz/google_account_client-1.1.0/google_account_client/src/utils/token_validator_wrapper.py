from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def ensure_valid_token(func):
    """
    ### @with_google_calendar
    
    Decorator that ensures the wrapped function receives an up to date authenticated Google Calendar API service.

    The wrapped function must accept `service` as its argument or keyargument.
    
    Useful for refreshing, and building of the service client and ensuring the credentials are valid.

    #### Returns:
        The return value of the wrapped function, with an injected `service`.
    """
    def wrapper(self, *args, **kwargs):
        if not self._user_token or not self._user_token.valid:
            if self._user_token and self._user_token.expired and self._user_token.refresh_token:
                self._user_token.refresh(Request())
                self._service = build('calendar', 'v3', credentials=self._user_token)
                self.log('Token refreshed!', 'info')
            else:
                self.log('Invalid credentials and no refresh token available.', 'error')
                raise RuntimeError('Invalid credentials and no refresh token available.')
        return func(self, *args, **kwargs)
    return wrapper