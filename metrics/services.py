import requests
from django.conf import settings

# Ensure a consistent base URL format
API_BASE = (settings.API_BASE_URL or '').rstrip('/')

DEFAULT_TIMEOUT = 5  # seconds

def get_jwt_token(username, password, role):
    if not (username and password and role and API_BASE):
        return None
    url = f'{API_BASE}/login'
    try:
        res = requests.post(url, json={'username': username, 'password': password, 'role': role}, timeout=DEFAULT_TIMEOUT)
        if res.ok:
            return res.json().get('access_token')
    except requests.RequestException:
        return None
    return None

def fetch_telemetry(jwt_token):
    if not (jwt_token and API_BASE):
        return []
    headers = {'Authorization': f'Bearer {jwt_token}'}
    try:
        res = requests.get(f'{API_BASE}/telemetry', headers=headers, timeout=DEFAULT_TIMEOUT)
        if res.ok:
            return res.json()  # Adjust if your API returns a different structure
    except requests.RequestException:
        return []
    return []
