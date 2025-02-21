#  substitue du views.py
# ce sont les méthodes

# substitue de views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.serializers import MissionSerializer, CandidatureSerializer
from app.models import Mission, Candidature, Formation

#Formation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Créer une mission
@api_view(['POST'])
def create_mission(request):
    serializer = MissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lister les missions
@api_view(['GET'])
def list_missions(request):
    missions = Mission.objects.all()
    serializer = MissionSerializer(missions, many=True)
    return Response(serializer.data)

# Récupérer une mission spécifique par son ID
@api_view(['GET'])
def get_mission(request, mission_id):
    try:
        mission = Mission.objects.get(id=mission_id)
        serializer = MissionSerializer(mission)
        return Response(serializer.data)
    except Mission.DoesNotExist:
        return Response({"error": "Mission non trouvée"}, status=status.HTTP_404_NOT_FOUND)

# Mettre à jour une mission
@api_view(['PUT'])
def update_mission(request, mission_id):
    try:
        mission = Mission.objects.get(id=mission_id)
        serializer = MissionSerializer(mission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Mission.DoesNotExist:
        return Response({"error": "Mission non trouvée"}, status=status.HTTP_404_NOT_FOUND)

# Supprimer une mission
@api_view(['DELETE'])
def delete_mission(request, mission_id):
    try:
        mission = Mission.objects.get(id=mission_id)
        mission.delete()
        return Response({"message": "Mission supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
    except Mission.DoesNotExist:
        return Response({"error": "Mission non trouvée"}, status=status.HTTP_404_NOT_FOUND)

# Créer une candidature
@api_view(['POST'])
def create_candidature(request):
    serializer = CandidatureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lister les candidatures
@api_view(['GET'])
def list_candidatures(request):
    candidatures = Candidature.objects.all()
    serializer = CandidatureSerializer(candidatures, many=True)
    return Response(serializer.data)

# Récupérer une candidature spécifique par son ID
@api_view(['GET'])
def get_candidature(request, candidature_id):
    try:
        candidature = Candidature.objects.get(id=candidature_id)
        serializer = CandidatureSerializer(candidature)
        return Response(serializer.data)
    except Candidature.DoesNotExist:
        return Response({"error": "Candidature non trouvée"}, status=status.HTTP_404_NOT_FOUND)

# Mettre à jour une candidature
@api_view(['PUT'])
def update_candidature(request, candidature_id):
    try:
        candidature = Candidature.objects.get(id=candidature_id)
        serializer = CandidatureSerializer(candidature, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Candidature.DoesNotExist:
        return Response({"error": "Candidature non trouvée"}, status=status.HTTP_404_NOT_FOUND)

# Supprimer une candidature
@api_view(['DELETE'])
def delete_candidature(request, candidature_id):
    try:
        candidature = Candidature.objects.get(id=candidature_id)
        candidature.delete()
        return Response({"message": "Candidature supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
    except Candidature.DoesNotExist:
        return Response({"error": "Candidature non trouvée"}, status=status.HTTP_404_NOT_FOUND)
    
#Formation

@csrf_exempt  # Permet de désactiver la protection CSRF pour cette vue (à utiliser avec précaution)
def mark_formation_completed(request, formation_id):
    if request.method == 'POST':
        try:
            # Récupérer les données de la requête
            data = json.loads(request.body)
            user_id = data.get('userId')  # Vous pouvez utiliser ceci pour identifier l'utilisateur

            # Récupérer la formation
            formation = Formation.objects.get(id=formation_id)

            # Marquer la formation comme terminée
            formation.is_completed = True
            formation.save()

            # Répondre avec un succès
            return JsonResponse({'message': 'Formation marquée comme terminée avec succès !'}, status=200)
        except Formation.DoesNotExist:
            return JsonResponse({'error': 'Formation non trouvée'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)