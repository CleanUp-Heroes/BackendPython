from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

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
    username = request.data.get('username')
    password = request.data.get('password')

    if not (username and password):
        return JsonResponse({"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)  # Authenticate using Django's built-in method

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
                # 'access': str(refresh.access_token),
                'token': str(refresh)
            }, status=status.HTTP_200_OK)

    
    return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

