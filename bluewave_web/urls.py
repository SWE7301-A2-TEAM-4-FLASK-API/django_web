"""
URL configuration for bluewave_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import user as user_profile_view
from django.views.generic import TemplateView
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # This makes 'index' available for {% url 'index' %}
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('subscriptions/', include('subscriptions.urls', namespace='subscriptions')),
    path('products/', include('products.urls', namespace='products')),
    path('metrics/', include('metrics.urls', namespace='metrics')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    # Alias to support templates referring to 'useraccount'
    path('useraccount/', TemplateView.as_view(template_name='useraccount.html'), name='useraccount'),
    # Two-factor authentication URLs
    path('account/', include('two_factor.urls')),
]