from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/suggest/', views.search_suggestions, name='search_suggestions'),
    path('teams/', views.get_teams, name='get_teams'),
    path('teams/join/<int:team_id>/', views.join_team, name='join_team'),
    path('upvote/<int:resource_id>/', views.upvote, name='upvote'),
]