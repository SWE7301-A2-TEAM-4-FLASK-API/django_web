from django.urls import path
from . import views

app_name = 'subscriptions'
urlpatterns = [
    path('', views.subscription_list, name='list'),
    path('subscribe/<int:product_id>/', views.subscribe, name='subscribe'),
]
