from rest_framework.views import APIView
from rest_framework.response import Response

class CandidatureList(APIView):
    def get(self, request):
        return Response({"message": "Liste des candidatures"})

class CandidatureDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détail de la candidature {pk}"})
