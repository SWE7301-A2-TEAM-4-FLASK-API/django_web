import requests
from django.conf import settings
import logging

API_BASE = (settings.API_BASE_URL or '').rstrip('/')
DEFAULT_TIMEOUT = 5  # seconds

def get_jwt_token(username, password, role):
    """
    Authenticate with the external API and return a JWT token.
    """
    if not (username and password and role and API_BASE):
        return None
    url = f'{API_BASE}/login'
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
    if not (jwt_token and API_BASE):
        return []
    headers = {'Authorization': f'Bearer {jwt_token}'}
    try:
        res = requests.get(f'{API_BASE}/telemetry', headers=headers, timeout=DEFAULT_TIMEOUT)
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
