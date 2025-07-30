import requests
import time

def authenticate_with_api_key(session: requests.Session, api_key: str, num_retry: int = 2, initial_delay: float = 0.5, exponential_backoff: float = 2.0, auth_base_url: str = "https://auth.svml.dev/v1") -> str:
    """
    Authenticates with the API key and returns the JWT access token.
    Retries according to the provided options.
    :param session: requests.Session for HTTP
    :param api_key: The API key string
    :param num_retry: Number of retries
    :param initial_delay: Initial delay between retries
    :param exponential_backoff: Backoff multiplier
    :param auth_base_url: Base URL for the auth API
    :return: The access token string
    :raises: Exception if authentication fails after all retries
    """
    delay = initial_delay
    for attempt in range(num_retry + 1):
        try:
            response = session.post(f'{auth_base_url}/api-keys/validate', json={"api_key": api_key})
            response.raise_for_status()
            data = response.json()
            access_token = data.get('access_token')
            if not access_token:
                raise Exception('No access_token returned from API')
            return access_token
        except Exception as e:
            if attempt < num_retry:
                time.sleep(delay)
                delay *= exponential_backoff
            else:
                raise

def fetch_metadata(session: requests.Session, token: str, api_base_url: str = "https://api.svml.dev/v1", num_retry: int = 2, initial_delay: float = 0.5, exponential_backoff: float = 2.0):
    """
    Fetches models and SVML versions from the metadata endpoints.
    :param session: requests.Session for HTTP
    :param token: Bearer token for authentication
    :param api_base_url: Base URL for the API
    :param num_retry: Number of retries
    :param initial_delay: Initial delay between retries
    :param exponential_backoff: Backoff multiplier
    :return: Dictionary with models and svml_versions
    """
    models = []
    svml_versions = []
    
    # Fetch models
    delay = initial_delay
    for attempt in range(num_retry + 1):
        try:
            models_response = session.get(
                f'{api_base_url}/models',
                headers={'Authorization': f'Bearer {token}'}
            )
            models_response.raise_for_status()
            models_data = models_response.json()
            models = [m.get('name') for m in models_data.get('models', []) if m.get('name')]
            break
        except Exception as e:
            if attempt < num_retry:
                time.sleep(delay)
                delay *= exponential_backoff
            else:
                # Don't fail completely, just continue with empty models list
                pass
    
    # Fetch SVML versions
    delay = initial_delay
    for attempt in range(num_retry + 1):
        try:
            versions_response = session.get(
                f'{api_base_url}/svml-versions',
                headers={'Authorization': f'Bearer {token}'}
            )
            versions_response.raise_for_status()
            versions_data = versions_response.json()
            svml_versions = versions_data.get('versions', [])
            break
        except Exception as e:
            if attempt < num_retry:
                time.sleep(delay)
                delay *= exponential_backoff
            else:
                # Don't fail completely, just continue with empty versions list
                pass
    
    return {
        'models': models,
        'svml_versions': svml_versions
    } 