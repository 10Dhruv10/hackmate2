from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/suggest/', views.search_suggestions, name='search_suggestions'),
    path('upvote/<int:resource_id>/', views.upvote, name='upvote'),
]