from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, RoleAuthenticationForm, ProfileForm
from subscriptions.models import Subscription
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from metrics.services import get_jwt_token

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('accounts:login')
            except Exception as e:
                messages.error(request, 'An unexpected error occurred. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

class AuthLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = RoleAuthenticationForm
    success_url = reverse_lazy('products:list')
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        # Use the provided login credentials to obtain a JWT for telemetry
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        role = form.cleaned_data.get('role')
        token = get_jwt_token(username, password, role)
        if token:
            self.request.session['api_jwt'] = token
            self.request.session['api_jwt_expiry'] = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
            self.request.session['api_role'] = role
        else:
            messages.warning(self.request, 'Logged in, but could not obtain live telemetry token. Demo data will be shown if enabled.')
        return response

def login_view(request):
    return AuthLoginView.as_view()(request)

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def user(request):
    # Generate token (use actual password or a service account if needed)
    token = get_jwt_token(request.user.username, None, request.user.role)
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'api_token': token,
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:user')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/update.html', {'form': form})

@login_required
def user_settings(request):
    return render(request, 'accounts/user_settings.html', {})
    
def enable_2fa(request):
    from django.shortcuts import render
    from django.core.mail import send_mail
    from django.conf import settings
    import random
    from django.contrib import messages

    token_sent = False
    user = request.user
    if request.method == 'POST':
        if 'send_token' in request.POST:
            token = str(random.randint(100000, 999999))
            request.session['2fa_token'] = token
            if user.phone_number:
                # Send token via SMS (Twilio or similar service)
                try:
                    from twilio.rest import Client
                    twilio_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
                    twilio_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
                    twilio_from = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
                    if twilio_sid and twilio_token and twilio_from:
                        client = Client(twilio_sid, twilio_token)
                        client.messages.create(
                            body=f'Your verification code is: {token}',
                            from_=twilio_from,
                            to=user.phone_number
                        )
                        messages.success(request, 'Verification code sent to your phone.')
                    else:
                        messages.error(request, 'SMS service not configured. Token not sent.')
                except Exception as e:
                    messages.error(request, f'Error sending SMS: {e}')
            else:
                send_mail(
                    'Your Two-Factor Authentication Code',
                    f'Your verification code is: {token}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Verification code sent to your email.')
            token_sent = True
        elif 'verify_token' in request.POST:
            entered_token = request.POST.get('token')
            session_token = request.session.get('2fa_token')
            if entered_token == session_token:
                user.is_2fa_enabled = True
                user.save()
                messages.success(request, 'Two-Factor Authentication enabled successfully!')
                if '2fa_token' in request.session:
                    del request.session['2fa_token']
                token_sent = False
            else:
                token_sent = True
                messages.error(request, 'Invalid token. Please try again.')
    return render(request, 'accounts/enable_2fa.html', {'token_sent': token_sent})
