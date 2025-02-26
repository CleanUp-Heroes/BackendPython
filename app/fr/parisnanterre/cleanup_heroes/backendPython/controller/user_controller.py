from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken, RefreshToken
import json
from app.models import ForumModerateur, AuthUser

@swagger_auto_schema(
    method='post',
    operation_description="Register a new user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "password", "first_name", "last_name"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email of the user"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password of the user"),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name of the user"),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name of the user"),
        },
    ),
    responses={
        201: "User created successfully",
        400: "Bad request - Validation errors",
    },
)
@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not (email and password and first_name and last_name):
        return JsonResponse({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    username = f"{first_name.lower()}.{last_name.lower()}"
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already in use"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)  # Hash the password securely
    user.save()

    return JsonResponse({"message": "User created successfully", "user_id": user.id, "username": username}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='post',
    operation_description="Log in a user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username of the user"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password of the user"),
        },
    ),
    responses={
        200: "Login successful",
        400: "Invalid credentials",
    },
)
@api_view(['POST'])
def login(request):
    try:
        data = json.loads(request.body)  # Récupérer les données JSON envoyées
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse(
                {"error": "Both username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)  # Méthode d'authentification

        if user is not None:
            token = RefreshToken.for_user(user)
            user = AuthUser.objects.get(username=username)
            is_moderator = ForumModerateur.objects.filter(user=user).exists()

            return JsonResponse({
                'token': str(token),
                'is_moderator': is_moderator,  
                'username' : username
            }, status=status.HTTP_200_OK)
            

        return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format"},
            status=status.HTTP_400_BAD_REQUEST
        )

@swagger_auto_schema(
    method='post',
    operation_description="Log out a user and blacklist the refresh token",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["Authorization"],
        properties={
            "Authorization": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token of the user"),
        },
    ),
    responses={
        200: "Logout successful",
        400: "Invalid or missing refresh token",
    },
)
@api_view(['POST'])
def logout(request):
    # Récupérer le refresh token depuis la requête
    token_value = request.headers.get('Authorization')

    if not token_value:
        return JsonResponse({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Créer un objet RefreshToken à partir du refresh token envoyé
        token = RefreshToken(token_value)

        # Révoquer ou blacklister ce refresh token
        token.blacklist()

        return JsonResponse({"message": "Logout successful, refresh token blacklisted."}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)