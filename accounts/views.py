from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, RoleAuthenticationForm
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
    subs = Subscription.objects.filter(user=request.user).select_related('product')
    return render(request, 'accounts/profile.html', {'subscriptions': subs})
