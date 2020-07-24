from os import name
from django.urls import path
from . import views
urlpatterns = [
    path('', views.get_tips, name='tips'),
    path('post/', views.add_tip, name='post'),
    path('edit/', views.end_fixture, name='edit'),
    path('odds', views.totalOdds, name='odds'),
    path('featured', views.featured_match, name='featured'),
    path('recent', views.recent_tips, name='recent'),
    path('del/<id>', views.delete_prediction, name='delete')
]