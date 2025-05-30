from rest_framework.views import APIView
from rest_framework.response import Response

class RelanceList(APIView):
    def get(self, request):
        return Response({"message": "Liste des relances"})

class RelanceDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détail de la relance {pk}"})
