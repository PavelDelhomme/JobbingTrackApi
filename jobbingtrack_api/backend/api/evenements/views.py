from rest_framework.views import APIView
from rest_framework.response import Response

class EvenementList(APIView):
    def get(self, request):
        return Response({"message": "Liste des événements"})

class EvenementDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détail de l'événement {pk}"})
