from rest_framework.views import APIView
from rest_framework.response import Response

class AppelList(APIView):
    def get(self, request):
        return Response({"message": "Liste des appels"})

class AppelDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détails de l'appel {pk}"})