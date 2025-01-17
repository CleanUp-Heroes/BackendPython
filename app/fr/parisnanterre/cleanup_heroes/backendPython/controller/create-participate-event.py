from django.http import JsonResponse
from rest_framework.decorators import api_view
from app.models import CleaningEvent, Participation
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User

# Swagger documentation for the POST method
@swagger_auto_schema(
    method='post',
    operation_description="Create a cleaning event by providing title, location, date, time, max participants, and an optional description.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['title', 'location', 'date', 'time', 'max_participants'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="The title of the event."),
            'location': openapi.Schema(type=openapi.TYPE_STRING, description="The location of the event."),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description="The date of the event."),
            'time': openapi.Schema(type=openapi.TYPE_STRING, description="The time of the event."),
            'max_participants': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum number of participants."),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="Optional description of the event."),
        },
    ),
    responses={
        201: openapi.Response(description="Event created successfully."),
        400: openapi.Response(description="Bad request."),
        500: openapi.Response(description="Internal server error."),
    }
)
@api_view(['POST'])
def create_event(request):
    if request.method == 'POST':
        token_value = request.headers.get('Authorization')

        if not token_value:
            raise AuthenticationFailed("Token is missing in the request.")

        user_id = None
        try:
            refresh_token = RefreshToken(token_value)
            user_id = refresh_token['user_id']

            user = User.objects.get(id=user_id)

            if not user.is_active:
                raise AuthenticationFailed('User is inactive.')
        except Exception:
            raise AuthenticationFailed("Invalid token or token does not exist.")

        try:
            # Retrieve form data
            title = request.data.get('title')
            location = request.data.get('location')
            date = request.data.get('date')
            time = request.data.get('time')
            max_participants = request.data.get('max_participants')
            description = request.data.get('description', '')

            # Validate required fields
            if not all([title, location, date, time, max_participants]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Create the event
            event = CleaningEvent.objects.create(
                title=title,
                location=location,
                date=date,
                time=time,
                max_participants=max_participants,
                description=description,
                creator=user
            )

            return JsonResponse({'message': 'Event created successfully', 'event_id': event.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@swagger_auto_schema(
    method='post',
    operation_description="Participate in an event by providing the event ID.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['event_id'],
        properties={
            'event_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the event to join."),
        },
    ),
    responses={
        201: openapi.Response(description="Participation registered successfully."),
        400: openapi.Response(description="Bad request."),
        500: openapi.Response(description="Internal server error."),
    }
)
@api_view(['POST'])
def participate_event(request):
    if request.method == 'POST':
        token_value = request.headers.get('Authorization')

        if not token_value:
            raise AuthenticationFailed("Token is missing in the request.")

        user_id = None
        try:
            refresh_token = RefreshToken(token_value)
            user_id = refresh_token['user_id']

            user = User.objects.get(id=user_id)

            if not user.is_active:
                raise AuthenticationFailed('User is inactive.')
        except Exception:
            raise AuthenticationFailed("Invalid token or token does not exist.")

        try:
            # Retrieve event ID
            event_id = request.data.get('event_id')

            # Validate event ID
            if not event_id:
                return JsonResponse({'error': 'Event ID is required'}, status=400)

            # Check if event exists
            event = CleaningEvent.objects.get(id=event_id)

            # Check if the user is already a participant
            if Participation.objects.filter(event=event, user=user).exists():
                return JsonResponse({'error': 'User already participating in this event'}, status=400)

            # Check if the event is full
            if event.participants.count() >= event.max_participants:
                return JsonResponse({'error': 'Event is full'}, status=400)

            # Register participation
            Participation.objects.create(event=event, user=user)

            return JsonResponse({'message': 'Participation registered successfully'}, status=201)

        except CleaningEvent.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@swagger_auto_schema(
    method='get',
    operation_description="Retrieve the user's event history, including past and upcoming events.",
    responses={
        200: openapi.Response(description="Event history retrieved successfully."),
        400: openapi.Response(description="Bad request."),
        500: openapi.Response(description="Internal server error."),
    }
)
@api_view(['GET'])
def event_history(request):
    try:
        token_value = request.headers.get('Authorization')

        if not token_value:
            raise AuthenticationFailed("Token is missing in the request.")

        user_id = None
        try:
            refresh_token = RefreshToken(token_value)
            user_id = refresh_token['user_id']

            user = User.objects.get(id=user_id)

            if not user.is_active:
                raise AuthenticationFailed('User is inactive.')
        except Exception:
            raise AuthenticationFailed("Invalid token or token does not exist.")

        # Retrieve the user's participation history
        participations = Participation.objects.filter(user=user).select_related('event')
        history = [
            {
                'event_id': p.event.id,
                'title': p.event.title,
                'location': p.event.location,
                'date': p.event.date,
                'time': p.event.time,
                'is_past': p.event.date < now().date(),
            }
            for p in participations
        ]

        return JsonResponse({'event_history': history}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
