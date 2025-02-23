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
from app.views import *
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

    path('classement/', challenge_controller.leaderboard_global, name='classement'),
    path('reports/resolve_report/', reporting_controller.resolve_report, name='resolve_report'),
    
    path('forum/create_topic/', forum_controller.create_topic, name='create_topic'),
    path('forum/categories/', forum_controller.get_forum_categories, name='get_forum_categories'),

    path('forum/topics/', forum_controller.get_forum_topics, name='get_forum_topics'),
    path('forum/topics/<int:topic_id>/vote/', forum_controller.vote_forum_topic, name='vote_forum_topic'),
    
    path('forum/topics/<int:topic_id>/', forum_controller.get_topic_detail, name='get_topic_detail'),
    path('forum/topics/<int:topic_id>/replies/', forum_controller.get_topic_replies, name='get_topic_replies'),
    path('forum/topics/<int:topic_id>/replies/add/', forum_controller.add_reply, name='add_reply'),
    path("forum/topics/<int:topic_id>/like/", forum_controller.like_topic, name="like_topic"),

    path("forum/report/subject/", forum_controller.report_subject, name="report_subject"),
    path("forum/report/response/", forum_controller.report_response, name="report_response"),
    path("forum/reports/", forum_controller.get_reports, name="get_reports"),

    path('moderation/reports/', forum_controller.list_reported_content, name='list_reported_content'),
    path('moderation/reports/<int:report_id>/moderate/', forum_controller.moderate_report, name='moderate_report'),
         
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # urls volontariat
    #path('recrutement/', include('recrutement.urls')),
#] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

