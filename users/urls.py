from os import name
from . import views
from django.urls import path

urlpatterns = [
    path('', views.users_list, name='users'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('makevip/', views.make_vip, name='makevip'),
    path('profile', views.user_profile, name='profile'),
    path('del/<id>', views.delete_user, name='del')
]