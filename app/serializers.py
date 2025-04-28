# serializers.py pour mission et candidature

from rest_framework import serializers
from .models import Mission, Candidature, ForumSujets


# pour afficher la liste des missions
class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'  # ou spécifie les champs que tu veux inclure, par exemple ['titre', 'description', 'date']


class CandidatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidature
        fields = '__all__'
        
class SujetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumSujets
        fields = '__all__'
