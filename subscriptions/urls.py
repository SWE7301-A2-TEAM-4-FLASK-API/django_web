from django.urls import path
from . import views

app_name = 'subscriptions'
urlpatterns = [
    path('', views.subscription_list, name='list'),
    path('subscribe/<int:product_id>/', views.subscribe, name='subscribe'),
    path('cancel/<int:sub_id>/', views.cancel_subscription, name='cancel'),
    path('toggle-renewal/<int:sub_id>/', views.toggle_renewal, name='toggle_renewal'),
]
