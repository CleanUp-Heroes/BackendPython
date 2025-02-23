from app.fr.parisnanterre.cleanup_heroes.backendPython.controller import  volontariat_controller, challenge_controller, reporting_controller, user_controller, forum_controller

# views.py pour la base de données du feature volontariat
#pour
#Lister les missions. j'ai mis volontariat-controller
#Lister les candidatures.
#Mettre à jour le statut d'une candidature.

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Mission, Candidature
from .serializers import MissionSerializer, CandidatureSerializer

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

class CandidatureViewSet(viewsets.ModelViewSet):
    queryset = Candidature.objects.all()
    serializer_class = CandidatureSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')

        if new_status in dict(Candidature.STATUS_CHOICES).keys():
            instance.status = new_status
            instance.save()
            return Response({"message": f"Statut mis à jour à {new_status}."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Statut invalide."}, status=status.HTTP_400_BAD_REQUEST)


# pour ajouter la liste des missions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Mission
from .serializers import MissionSerializer

class MissionList(APIView):
    def get(self, request):
        missions = Mission.objects.all()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
