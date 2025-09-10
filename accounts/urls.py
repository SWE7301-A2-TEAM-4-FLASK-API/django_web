from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user, name='user'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/settings/', views.user_settings, name='user_settings'),
    path('profile/update/', views.edit_profile, name='update'),
]
