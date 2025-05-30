from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileList(APIView):
    def get(self, request):
        return Response({"message": "Liste des profils"})

class ProfileDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détail du profil {pk}"})
