# challenges/serializers.py
#Utilisation de pour convertir les données du modèle Challenge en JSON pour les API.

from rest_framework import serializers
from .models import Challenge, Participation

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'
