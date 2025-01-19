# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MissionViewSet, CandidatureViewSet

router = DefaultRouter()
router.register(r'missions', MissionViewSet)
router.register(r'candidatures', CandidatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]