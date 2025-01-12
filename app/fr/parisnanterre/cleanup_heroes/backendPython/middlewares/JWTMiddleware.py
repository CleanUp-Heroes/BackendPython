from django.http import JsonResponse
from django.conf import settings
import jwt
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import TokenBlacklistBlacklistedtoken, TokenBlacklistOutstandingtoken
from datetime import datetime, timezone

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Liste des routes qui ne nécessitent PAS d'authentification
        self.excluded_routes = [
            '/login/',  
            '/register/',  
        ]

    def __call__(self, request):
        # Si la route actuelle n'est pas dans la liste des routes non protégées
        if request.path not in self.excluded_routes:
            token = request.headers.get('Authorization')
            if not token:
                return JsonResponse({"error": "Token is missing"}, status=401)

            try:
                # Décodage du token sans vérifier la signature (si on souhaite vérifier uniquement expiration pour un refresh_token)
                decoded_token = jwt.decode(token, options={"verify_signature": False})
                
                # Vérification de l'expiration du token
                expiration_timestamp = decoded_token.get("exp")
                if not expiration_timestamp:
                    return JsonResponse({"error": "Expiration claim (exp) not found in token"}, status=401)

                # Convertir le timestamp en datetime UTC
                expiration_date = datetime.fromtimestamp(expiration_timestamp, tz=timezone.utc)
                if expiration_date < datetime.now(timezone.utc):
                    return JsonResponse({"error": "Token has expired"}, status=401)
                
                # Vérification si le refresh token existe et est valide
                refresh_token = decoded_token.get('token')
                if refresh_token:
                    token_id = TokenBlacklistOutstandingtoken.objects.filter(token=refresh_token).first().id
                    if TokenBlacklistBlacklistedtoken.objects.filter(id=token_id).exists():
                        return JsonResponse({"error": "Refresh token is invalid"}, status=401)
            
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except jwt.InvalidTokenError as e:
                return JsonResponse({"error": str(e)}, status=401)

        return self.get_response(request)
