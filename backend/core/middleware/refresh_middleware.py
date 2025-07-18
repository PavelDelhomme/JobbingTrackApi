from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse

class RefreshMiddleware:
    """Force le refresh automatique si le token est expiré et que le refresh est encore valide.
    (Optionnel : généralement géré côté mobile)"""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth.split()[1]
            try:
                AccessToken(token)
            except TokenError:
                return JsonResponse({'detail': 'Token expiré'}, status=401)
        return self.get_response(request)