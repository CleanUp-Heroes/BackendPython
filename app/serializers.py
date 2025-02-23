# serializers.py
from rest_framework import serializers
from .models import Mission, Candidature, ForumSujets

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'

class CandidatureSerializer(serializers.ModelSerializer):
    mission = MissionSerializer(read_only=True)

    class Meta:
        model = Candidature
        fields = '__all__'
        
class SujetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumSujets
        fields = '__all__'