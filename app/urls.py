from django.urls import path
from .views import MissionList

urlpatterns = [
    path('api/missions/', MissionList.as_view(), name='mission-list'),
    # autres URLs
]
