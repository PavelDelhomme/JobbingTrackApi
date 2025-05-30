from rest_framework.views import APIView
from rest_framework.response import Response

class EntrepriseList(APIView):
    def get(self, request):
        return Response({"message": "Liste des entreprises"})

class EntrepriseDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détail de l'entreprise {pk}"})
