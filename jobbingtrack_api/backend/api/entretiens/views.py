from rest_framework.views import APIView
from rest_framework.response import Response

class EntretienList(APIView):
    def get(self, request):
        return Response({"message": "Liste des entretiens"})

class EntretienDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détail de l'entretien {pk}"})
