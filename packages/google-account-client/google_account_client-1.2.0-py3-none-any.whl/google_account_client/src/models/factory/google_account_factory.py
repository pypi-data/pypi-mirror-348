from ..service_handler import TokenLoader, OAuthService
from ..google_account import GoogleAccount
from ...settings import Config
from ...utils import logs

class GoogleAccountFactory():
    def __init__(self, client_secrets: str, enable_logs: bool = None):
        """
        Factory to create GoogleAccount instances using a shared client secret (OAuth client).

        Args:
            client_secrets (str | dict): Path to the OAuth client secrets JSON file.
            logging (int): Port for the local server flow to listen on.
            enable_logs (bool): If True, enables debug/info logging.
        """
        # Single Responsability
        self._token_loader = TokenLoader()
        self._oauth_service = OAuthService(client_secrets)
        
        configs = {
            'enable_logs': enable_logs
        }
        Config.update_configs(configs)
        
    def is_valid_token(self, user_token) -> bool:
        logs.newline()
        logs.log('Consulting token validity:', 'info')
        return self._token_loader.is_valid_token(user_token)
    
    def generate_authorization_url(self, redirect_uri: str) -> tuple[str, str]:
        """
        Creates a link to authenticate the user.

        Args:
            name (str): Account identifier.
            redirect_uri (str): callback URL.
        
        Returns:
            tuple[str, str]: The authentication URL and the state.
        """
        logs.newline()
        logs.log('Creating OAuth link...', 'info')
        
        return self._oauth_service.generate_authorization_url(redirect_uri)
    
    def fetch_token_from_redirect(self, redirected_url, expected_state = None):
        """
        Fetches the token from the redirected URL after user authentication.

        Args:
            redirected_url (str): URL after user authentication.
            expected_state (str, optional): Expected state parameter from the authorization URL.
            
        Returns:
            Credentials: The user's credentials.
        """
        logs.log(f'Fetching token from redirect...', 'info')
        
        return self._oauth_service.fetch_token_from_redirect(redirected_url, expected_state)
    

    def load_account(self, name: str, user_token: any = None) -> GoogleAccount:
        """
        Creates a new GoogleAccount instance with valid credentials.

        Args:
            name (str): Account identifier.
            token (str | dict | Credentials, optional): Path, dict or Credentials instance for the user token.

        Returns:
            GoogleAccount
        """
        logs.newline()
        logs.log(f'Loading account \'{name}\':', 'info')
        
        try:
            user_token = self._token_loader.load(user_token)
        except:
            raise Exception('Invalid token.')

        account = GoogleAccount(
            name=name,
            user_token=user_token
        )
        
        logs.log('Account loaded successfully!', 'info')
        return account