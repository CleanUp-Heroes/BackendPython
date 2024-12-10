# challenges/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # La page d'accueil
    path('challenges/', views.challenge_list, name='challenge_list'),  # Liste des défis
    path('challenge/create/', views.ChallengeCreateView.as_view(), name='challenge_create'),  # Création de défi
    path('challenge/stats/', views.ChallengeStatsView.as_view(), name='challenge_stats'),  # Statistiques des défis
]