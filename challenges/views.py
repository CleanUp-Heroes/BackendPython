from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Challenge, Participation
from .serializers import ChallengeSerializer, ParticipationSerializer

class ChallengeView(APIView):
    def get(self, request):
        challenges = Challenge.objects.all()
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParticipationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# creation de view pour la page d'acceuil
from django.http import HttpResponse

def home(request):
    return HttpResponse("Bienvenue sur la page d'accueil de l'application!")

