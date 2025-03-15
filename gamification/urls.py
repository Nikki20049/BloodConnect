from django.urls import path
from . import views

urlpatterns = [
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('badges/', views.badges, name='badges'),
    path('badges/user/<str:username>/', views.user_badges, name='user_badges'),
]