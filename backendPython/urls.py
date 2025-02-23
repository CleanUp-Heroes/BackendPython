"""
URL configuration for backendPython project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from app.views import * # ça import toutes les méthodes mis dans view.py
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('challenges/statistics/', challenge_controller.get_challenges_statistiques, name='get_challenges_statistics'),
    path('challenges/unparticipated/', challenge_controller.get_unparticipated_challenges, name='get_unparticipated_challenges'),
    path('challenges/participation/', challenge_controller.add_participation, name='add_participation'),
    path('reports/report/', reporting_controller.add_report, name='add_report'),
    path('reports/get_reports/', reporting_controller.get_reports, name='get_report'),
    path('register/', user_controller.register, name='register'),
    path('login/', user_controller.login, name='login'),
    path('logout/', user_controller.logout, name='logout'),
    # urls volontariat
    #path('recrutement/', include('recrutement.urls')),
    #urls Mission et Candidature
    # urls.py

    
    #  Routes pour les missions
    path('volontariat/missions/', volontariat_controller.list_missions, name='list-missions'),  #  Liste toutes les missions
    path('volontariat/missions/create/', volontariat_controller.create_mission, name='create-mission'),  #  Créer une mission
    path('volontariat/missions/<int:id>/', volontariat_controller.get_mission, name='get-mission'),  #  Obtenir une mission spécifique
    path('volontariat/missions/<int:id>/update/', volontariat_controller.update_mission, name='update-mission'),  #  Mettre à jour une mission
    path('volontariat/missions/<int:id>/delete/', volontariat_controller.delete_mission, name='delete-mission'),  #  Supprimer une mission

    #  Routes pour les candidatures
    path('volontariat/candidatures/', volontariat_controller.list_candidatures, name='list-candidatures'),  # Liste des candidatures
    path('volontariat/candidatures/create/', volontariat_controller.create_candidature, name='create-candidature'),  #  Ajouter une candidature
    path('volontariat/candidatures/<int:id>/', volontariat_controller.get_candidature, name='get-candidature'),  #  Obtenir une candidature spécifique
    path('volontariat/candidatures/<int:id>/update/', volontariat_controller.update_candidature, name='update-candidature'),  #  Mettre à jour une candidature
    path('volontariat/candidatures/<int:id>/delete/', volontariat_controller.delete_candidature, name='delete-candidature'),  #  Supprimer une candidature

    # Route pour la formation 
    path('formations/list_user_formation/', volontariat_controller.list_user_formation, name='mark_formation_completed'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)