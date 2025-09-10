# metrics/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from .services import get_jwt_token, fetch_telemetry
from datetime import datetime, timedelta
from django.contrib import messages
from .models import Metric

@login_required
def dashboard(request):
    # Try to reuse cached JWT from session if it hasn't expired
    jwt_token = request.session.get('api_jwt')
    jwt_expiry = request.session.get('api_jwt_expiry')

    def token_is_valid(expiry):
        try:
            return expiry and datetime.fromisoformat(expiry) > datetime.utcnow()
        except Exception:
            return False

    if not jwt_token or not token_is_valid(jwt_expiry):
        # Try to obtain a new token using env service account
        username = settings.API_USERNAME
        password = settings.API_PASSWORD
        role = settings.API_ROLE or getattr(request.user, 'role', None)
        jwt_token = get_jwt_token(username, password, role) if (username and password and role) else None
        # Cache for 10 minutes to avoid frequent auth
        if jwt_token:
            request.session['api_jwt'] = jwt_token
            request.session['api_jwt_expiry'] = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    telemetry_data = fetch_telemetry(jwt_token) if jwt_token else []
    used_demo = False

    # DEBUG-friendly demo data to make the page useful during development
    if not telemetry_data and settings.DEBUG:
        telemetry_data = [
            { 'data': {
                'id': 1,
                'salinity': 35.1,
                'pH': 8.1,
                'temperature': 22.5,
                'location': 'Dock A',
                'timestamp': datetime.utcnow().isoformat(timespec='seconds')
            }},
            { 'data': {
                'id': 2,
                'salinity': 34.8,
                'pH': 8.0,
                'temperature': 21.9,
                'location': 'Dock B',
                'timestamp': datetime.utcnow().isoformat(timespec='seconds')
            }},
        ]
    used_demo = True
    messages.info(request, 'Showing demo telemetry (DEBUG mode). Configure API_* env vars to fetch live data.')

    # Normalize a flat API shape into the template’s expected {data:{...}} shape
    normalized = []
    for rec in telemetry_data or []:
        if isinstance(rec, dict) and 'data' in rec:
            normalized.append(rec)
        elif isinstance(rec, dict):
            normalized.append({'data': rec})
        else:
            # Fallback: wrap primitives
            normalized.append({'data': {'value': rec}})

    telemetry_source = 'demo' if used_demo else ('live' if normalized else 'none')
    metrics = Metric.objects.all()
    return render(request, 'metrics/dashboard.html', {
        'telemetry': normalized,
        'telemetry_source': telemetry_source,
        'metrics': metrics,
    })

