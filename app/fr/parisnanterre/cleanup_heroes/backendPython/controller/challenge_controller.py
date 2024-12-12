from django.http import JsonResponse
from app.models import *
from django.db.models import Sum
from datetime import date
import json

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view


@swagger_auto_schema(
    method='post',
    operation_description="Retrieve statistics about a user's challenges.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username of the user."),
        },
        required=['username'],
    ),
    responses={
        200: openapi.Response(
            description="Statistics about user's challenges.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "completed_challenges_count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of challenges completed by the user."),
                    "completed_challenges_list": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "challenge_name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the challenge."),
                                "completion_date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="Completion date of the challenge."),
                            },
                        ),
                    ),
                    "quantities": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        additional_properties=openapi.Schema(type=openapi.TYPE_INTEGER, description="Total quantity for each unit."),
                    ),
                    "progress": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "challenge_name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the challenge."),
                                "progress_percentage": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="Progress percentage."),
                                "realized_quantity": openapi.Schema(type=openapi.TYPE_STRING, description="Realized vs expected quantity with units."),
                                "unit": openapi.Schema(type=openapi.TYPE_STRING, description="Unit of measurement (e.g., kg, pieces)."),
                            },
                        ),
                    ),
                },
            ),
        ),
        404: openapi.Response(description="User not found."),
    },
)
@api_view(['POST'])
# Function to retrieve the statistics of a user's challenges
def get_challenges_statistiques(request):
    try:
        # Extract username from JSON body
        body = json.loads(request.body)
        username = body.get("username")
        
        # Find the user by username
        user = User.objects.get(name=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    # Count of completed challenges
    completed_challenges = CompletedChallenge.objects.filter(user_id=user.id)

    # List of completed challenges with their completion date
    completed_challenges_data = [
        {
            "challenge_name": completed_challenge.challenge.name,
            "completion_date": completed_challenge.completion_date
        }
        for completed_challenge in completed_challenges
    ]

    # Total quantity of actions performed by the user
    quantities_by_unit = (
        Participation.objects
        .filter(user_id=user.id)  # Filter participations by user
        .values('challenge__unit__name')  # Group by unit name
        .annotate(total=Sum('action_quantity'))  # Sum of quantities (action_quantity)
    )

    # Format the results for total quantity achieved
    quantities_data = {
        unit['challenge__unit__name']: unit['total'] or 0
        for unit in quantities_by_unit
    }

    # Progression on ongoing challenges
    progress_data = get_progress(user)

    # Return the statistics in a JSON response
    response_data =  {
        "completed_challenges_count": completed_challenges.count(),
        "completed_challenges_list": completed_challenges_data,
        "quantities": quantities_data,
        "progress": progress_data,
    }
    
    return JsonResponse(response_data, status=200)

# Function to retrieve the progress of the user on ongoing challenges
def get_progress(user):
    # Get the participations of the user for ongoing challenges (those that have not yet ended)
    ongoing_participations = Participation.objects.filter(user_id=user.id, challenge__end_date__gte=date.today())

    progress_data = []
    
    # Iterate over each ongoing participation and calculate the progress
    for participation in ongoing_participations:
        challenge = participation.challenge
        
        # Expected quantity for this challenge (in kg or pieces)
        expected_quantity = challenge.expected_actions  # Expected quantity for the challenge
        unit = challenge.unit.name  # Unit for the challenge, e.g., 'kg' or 'pieces'
        
        # Quantity performed by the user in this challenge
        total_realized_quantity = Participation.objects.filter(
            user_id=user.id, 
            challenge_id=challenge.id
        ).aggregate(total=Sum('action_quantity'))['total'] or 0  # Sum of quantities performed
        
        # Calculate the progress percentage
        if expected_quantity > 0:
            progress_percentage = (total_realized_quantity / expected_quantity) * 100
        else:
            progress_percentage = 0  # If the expected quantity is 0, set the progress percentage to 0

        # Add the progress data to the result list
        progress_data.append({
            'challenge_name': challenge.name,
            'progress_percentage': progress_percentage,
            'realized_quantity': f"{total_realized_quantity}/{expected_quantity} {unit}",  # Quantity realized / expected
            'unit': unit
        })
    
    return progress_data

@swagger_auto_schema(
    method='post',
    operation_description="Retrieve a list of challenges a user has not participated in.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username of the user."),
        },
        required=['username'],
    ),
    responses={
        200: openapi.Response(
            description="List of challenges the user has not participated in.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "unparticipated_challenges": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the challenge."),
                                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the challenge."),
                                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Description of the challenge."),
                            },
                        ),
                    ),
                },
            ),
        ),
        404: openapi.Response(description="User not found."),
    },
)
@api_view(['POST'])
def get_unparticipated_challenges(request):
    # Extraire les données JSON
    body = json.loads(request.body)
    username = body.get("username")
    
    # Vérifier si l'utilisateur existe
    try:
        user = User.objects.get(name=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    # Obtenir tous les IDs des défis auxquels l'utilisateur a participé
    participated_challenge_ids = Participation.objects.filter(user_id=user.id).values_list('challenge_id', flat=True)
    
    # Obtenir les défis auxquels l'utilisateur n'a pas participé
    unparticipated_challenges = Challenge.objects.exclude(id__in=participated_challenge_ids)
    
    # Formater les données pour la réponse
    challenges_data = [{"id": challenge.id, "name": challenge.name, "description": challenge.description} for challenge in unparticipated_challenges]
    
    return JsonResponse({"unparticipated_challenges": challenges_data}, status=200)