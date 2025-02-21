# serializers.py pour mission et candidature

from rest_framework import serializers
from .models import Mission, Candidature

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'  # Pour inclure tous les champs
        

class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = '__all__'
