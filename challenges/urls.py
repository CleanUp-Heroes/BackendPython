# challenges/urls.py
from django.urls import path
from .views import ChallengeCreateView, ChallengeStatsView

from django.contrib import admin
from django.urls import path, include
from challenges import views  # Importer la vue depuis l'application challenges

urlpatterns = [
    path('challenge/', ChallengeCreateView.as_view(), name='challenge-create'),
    path('challenge/stats/', ChallengeStatsView.as_view(), name='challenge-stats'),
    
    path('', views.home, name='home'),  # La vue pour la racine
    path('admin/', admin.site.urls),
    path('swagger/', include('swagger.urls')),
    path('challenge/', include('challenges.urls')),
    # Autres routes...
]


