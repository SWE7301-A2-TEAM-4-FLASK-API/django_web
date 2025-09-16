import requests
from django.conf import settings
import logging

def _api_base():
    return (getattr(settings, 'API_BASE_URL', '') or '').rstrip('/')

def _api_calls_enabled():
    return getattr(settings, 'API_CALLS_ENABLED', True)
DEFAULT_TIMEOUT = 30  # seconds

def get_jwt_token(username, password, role):
    """
    Authenticate with the external API and return a JWT token.
    """
    if not _api_calls_enabled():
        return None
    base = _api_base()
    if not (username and password and role and base):
        return None
    url = f'{base}/login'
    try:
        res = requests.post(url, json={'username': username, 'password': password, 'role': role}, timeout=DEFAULT_TIMEOUT)
        if res.ok:
            return res.json().get('access_token')
        else:
            logging.warning(f"JWT token request failed: {res.status_code} {res.text}")
    except requests.RequestException as e:
        logging.error(f"JWT token request exception: {e}")
    return None

def fetch_telemetry(jwt_token):
    """
    Fetch telemetry data from the external API using the JWT token.
    """
    if not _api_calls_enabled():
        return []
    base = _api_base()
    if not (jwt_token and base):
        return []
    headers = {'Authorization': f'Bearer {jwt_token}'}
    try:
        res = requests.get(f'{base}/telemetry', headers=headers, timeout=DEFAULT_TIMEOUT)
        if res.ok:
            data = res.json()
            # If your API wraps data in a key, adjust here:
            if isinstance(data, dict) and 'data' in data:
                return data['data']
            return data
        else:
            logging.warning(f"Telemetry fetch failed: {res.status_code} {res.text}")
    except requests.RequestException as e:
        logging.error(f"Telemetry fetch exception: {e}")
    return []
