from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view


@swagger_auto_schema(
    method='post',  # Spécifie que cette documentation concerne uniquement la méthode POST
    operation_description="Register a new user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["first_name", "last_name", "email", "password", "date_of_birth"],
        properties={
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name of the user"),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name of the user"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email of the user"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password of the user"),
            "date_of_birth": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="Date of birth (YYYY-MM-DD)"),
        },
    ),
    responses={
        201: "User created successfully",
        400: "Bad request - Validation errors",
    },
)
@api_view(['POST'])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    date_of_birth = request.data.get('date_of_birth')
    print(first_name, last_name, email, date_of_birth)

    if not (first_name and last_name and email and date_of_birth):
        return JsonResponse({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        date_of_birth=date_of_birth
    )

    return JsonResponse({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='get',  # Spécifie que cette documentation concerne uniquement la méthode GET
    operation_description="Log in a user",
    manual_parameters=[
        openapi.Parameter(
            name="username",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Email of the user",
            required=True
        )
    ],
    responses={
        200: "Login successful",
        400: "Invalid credentials",
    },
)
@api_view(['GET'])
def login(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({"error": "username is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(first_name=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "invalid username"}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
