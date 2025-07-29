import json

class FactoryServiceMethods:
    def _load_client_secrets(self, client_secrets: str) -> dict:
        if isinstance(client_secrets, str):
            try:
                with open(client_secrets, 'r') as f:
                    client_secrets = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f'Client secrets file not found: {client_secrets}.')
                
        if not isinstance(client_secrets, dict):
            raise TypeError(f'Client secrets must be a path or a dict, not {type(client_secrets)}.')
            
        return client_secrets