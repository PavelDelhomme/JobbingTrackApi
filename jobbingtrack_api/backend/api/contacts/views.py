from rest_framework.views import APIView
from rest_framework.response import Response

class ContactList(APIView):
    def get(self, request):
        return Response({"message": "Liste des contacts"})

class ContactDetail(APIView):
    def get(self, request, pk):
        return Response({"message": f"Détail du contact {pk}"})
