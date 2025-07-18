# backend/logic/authentication_service.py
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class AuthenticationService:
    @staticmethod
    def revoke_all_tokens(user):
        OutstandingToken.objects.filter(user=user).delete()
