from django.http import JsonResponse
from app.models import Participation, CompletedChallenge, Challenge, Proof, Userscore
from django.db.models import Sum
from datetime import date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ObjectDoesNotExist
from app.fr.parisnanterre.cleanup_heroes.backendPython.utils.utils import save_uploaded_file
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from django.db.models import Q

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve statistics about a user's challenges.",
    manual_parameters=[  # Utilisation de query params pour GET
        openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Username of the user.", required=True),
    ],
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
@api_view(['GET'])
def get_challenges_statistiques(request):
    # Récupérer le token depuis l'en-tête 'Authorization'
    token_value = request.headers.get('Authorization')
    if not token_value:
        raise AuthenticationFailed("Token is missing in the request.")
    
    # Vérifier la validité du token
    try:
        refresh_token = RefreshToken(token_value)
        user_id = refresh_token['user_id']
        user = User.objects.get(id=user_id)
        if not user.is_active:
            raise AuthenticationFailed('User is inactive.')
    except ValueError:
        raise AuthenticationFailed("Invalid token or token does not exist.")
    
    # Nombre total de défis complétés
    completed_challenges = CompletedChallenge.objects.filter(user_id=user.id)
    completed_challenges_data = [
        {
            "challenge_name": completed_challenge.challenge.name,
            "completion_date": completed_challenge.completion_date
        }
        for completed_challenge in completed_challenges
    ]

    # Quantités totales réalisées par unité
    total_quantity = (
        Participation.objects.filter(user_id=user.id)
        .values('challenge__unit__name')
        .annotate(total=Sum('action_quantity'))
    )
    total_quantity_data = [
        f"{item['total'] or 0} {item['challenge__unit__name']}" for item in total_quantity
    ]

    # Progression sur les défis en cours non complétés
    progress_data = get_progress(user)

    # Score total
    total_score = completed_challenges.aggregate(
        total_points=Sum('challenge__points')
    )['total_points'] or 0

    # Réponse avec toutes les données
    response_data = {
        "completedChallengesCount": completed_challenges.count(),
        "completedChallenges": completed_challenges_data,
        "totalQuantity": total_quantity_data,
        "progress": progress_data,
        "totalScore": total_score,
    }
    return JsonResponse(response_data, status=200)

def get_progress(user):
    # Obtenir les participations en cours, exclure les défis complétés
    completed_challenge_ids = CompletedChallenge.objects.filter(user_id=user.id).values_list('challenge_id', flat=True)
    participations = Participation.objects.filter(
        user_id=user.id,
        challenge__end_date__gte=date.today(),
    ).exclude(challenge_id__in=completed_challenge_ids)
    
    progress_dict = {}  # Utilisé pour éviter les doublons

    for participation in participations:
        challenge = participation.challenge
        if challenge.id in progress_dict:
            continue  # Éviter les doublons dans la progression

        expected_quantity = challenge.expected_actions
        unit = challenge.unit.name
        realized_quantity = (
            Participation.objects.filter(user_id=user.id, challenge_id=challenge.id)
            .aggregate(total=Sum('action_quantity'))['total'] or 0
        )

        progress_percentage = round((realized_quantity / expected_quantity) * 100, 2) if expected_quantity > 0 else 0
        progress_dict[challenge.id] = {
            "challengeName": challenge.name,
            "progressPercentage": progress_percentage,
            "realizedQuantity": f"{realized_quantity}/{expected_quantity} {unit}",
            "unit": unit,
        }

    return list(progress_dict.values())

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of challenges a user has not participated in.",
    manual_parameters=[  
        openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Username of the user.", required=True),
    ],
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
@api_view(['GET'])
def get_unparticipated_challenges(request):
    token_value = request.headers.get('Authorization')
    
    if not token_value:
        raise AuthenticationFailed("Token is missing in the request.")
    
    user = None
    # Vérifier la validité du token
    try:
        refresh_token = RefreshToken(token_value)
        user_id = refresh_token['user_id']
        
        user = User.objects.get(id=user_id)
        
        if not user.is_active:
                raise AuthenticationFailed('User is inactive.')
    except ValueError:
        raise AuthenticationFailed("Invalid token or token does not exist.")
    
    participated_challenge_ids = CompletedChallenge.objects.filter(user_id=user.id).values_list('challenge_id', flat=True)
    unparticipated_challenges = Challenge.objects.exclude(id__in=participated_challenge_ids)
    
    challenges_data = [
            {
            "id": challenge.id,
            "name": challenge.name,
            "description": challenge.description,
            "start_date": challenge.start_date,
            "end_date": challenge.end_date,
            "expected_actions": challenge.expected_actions,
            "unit": challenge.unit.name,
            "points": challenge.points
            }
        for challenge in unparticipated_challenges
    ]
    
    return JsonResponse({"unparticipated_challenges": challenges_data}, status=200)

@swagger_auto_schema(
    method='post',
    operation_description="Add a participation to a challenge, including an optional photo proof.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'challenge_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the challenge."),
            'action_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Date of the action taken."),
            'action_quantity': openapi.Schema(type=openapi.TYPE_NUMBER, description="Quantity of action performed (e.g., waste collected in kg)."),
            'challenge_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the challenge."),
            'photo': openapi.Schema(type=openapi.TYPE_FILE, description="Optional photo to prove the participation."),
        },
        required=['challenge_id', 'action_date', 'action_quantity', 'challenge_name'],
    ),
    responses={
        201: openapi.Response(
            description="Participation added successfully.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message."),
                },
            ),
        ),
        400: openapi.Response(
            description="Missing required fields or invalid data.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message."),
                },
            ),
        ),
        404: openapi.Response(description="Challenge not found."),
        405: openapi.Response(description="Invalid request method."),
        500: openapi.Response(description="Server error."),
    },
)
@api_view(['POST'])
def add_participation(request):
    if request.method == 'POST':
        token_value = request.headers.get('Authorization')
        
        if not token_value:
            raise AuthenticationFailed("Token is missing in the request.")
        
        user = None
        try:
            refresh_token = RefreshToken(token_value)
            user_id = refresh_token['user_id']
            
            user = User.objects.get(id=user_id)
            
            if not user.is_active:
                    raise AuthenticationFailed('User is inactive.')
        except ValueError:
            raise AuthenticationFailed("Invalid token or token does not exist.")
   
        try:
            # Récupérer les données des champs du formulaire
            challenge_id = request.data.get('challenge_id')
            action_date = request.data.get('date')
            action_quantity = request.data.get('quantity')

            required_fields = [challenge_id, action_date, action_quantity]
            
            missing_fields = [field for field, value in zip(required_fields, [challenge_id, action_date, action_quantity]) if not value]

            if missing_fields:
                return JsonResponse({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)

            # Vérifier si un fichier photo est envoyé dans la requête
            if 'photo' not in request.FILES:
                return JsonResponse({'error': 'Photo file is required'}, status=400)

            # Vérifier si le challenge existe
            try:
                challenge = Challenge.objects.get(id=challenge_id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Challenge not found'}, status=404)
            
            photo = request.FILES['photo']
            photo_url = save_uploaded_file(photo)

            proof = Proof.objects.create(photo=photo_url, creation_date=timezone.now())

            Participation.objects.create(
                user_id=user_id,
                challenge=challenge,
                action_quantity=action_quantity,
                action_date=action_date,
                photo_id=proof.id,
            )
            
            check_and_update_completed_challenges(user_id, challenge)

            return JsonResponse({'message': 'Participation and proof added successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def check_and_update_completed_challenges(user_id, challenge):
    # Vérifie si l'utilisateur a atteint ou dépassé la quantité attendue pour un défi et marque le défi comme complété si ce n'est pas déjà fait.

    # Calculer la somme totale des quantités (en forçant le résultat à un entier)
    total_quantity = int(
        Participation.objects.filter(
            user_id=user_id,
            challenge_id=challenge.id,
            action_date__range=[challenge.start_date, challenge.end_date]  # Début et fin du défi
        ).aggregate(total=Sum('action_quantity'))['total'] or 0
    )

    # Si la quantité totale est égale ou supérieure à la quantité attendue
    if total_quantity >= challenge.expected_actions:
        print("Quantité suffisante pour compléter le défi.")
        
        # Vérifier si ce défi n'est pas déjà marqué comme complété
        if not CompletedChallenge.objects.filter(user_id=user_id, challenge_id=challenge.id).exists():
            print("Marquage du défi comme complété.")
            
            # Ajouter le défi comme complété
            CompletedChallenge.objects.create(
                user_id=user_id,
                challenge=challenge,
                completion_date=now()
            )
            
            # Ajoute au score total le score du défi complété
            user_score = Userscore.objects.get(user__id=user_id)
            user_score.total_score += challenge.points
            user_score.save()    

@api_view(['GET'])
def leaderboard_global(request):
    if not request.headers.get('Authorization'):
        raise AuthenticationFailed("Token is missing in the request.")
    
    leaderboard = Userscore.objects.order_by('-total_score')
    data = [
        {
        "username": score.user.username, 
        "total_score": score.total_score} 
        
        for score in leaderboard
        ]
    
    return JsonResponse({"classement" : data}, status=200)