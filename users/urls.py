from os import name
from . import views
from django.urls import path

urlpatterns = [
    path('', views.users_list, name='users'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile', views.user_profile, name='profile')
]