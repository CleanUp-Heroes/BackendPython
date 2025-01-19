from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view
from app.models import Report, Proof, ReportResolved
from app.fr.parisnanterre.cleanup_heroes.backendPython.utils.utils import save_uploaded_file, validate_required_fields
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
import os, base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


# Swagger documentation for the POST method
@swagger_auto_schema(
    method='post',
    operation_description="Create a report by submitting a description, address, photo (file), and user ID.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['description', 'adresse', 'photo'],
        properties={
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="The description of the report."),
            'adresse': openapi.Schema(type=openapi.TYPE_STRING, description="The address where the report was made."),
            'photo': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description="A photo associated with the report (file)."),
        },
    ),
    responses={  # Define success and error responses
        201: openapi.Response(description="Report created successfully."),
        400: openapi.Response(description="Bad request."),
        500: openapi.Response(description="Internal server error."),
    }
)
@api_view(['POST'])
def add_report(request):
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
        except ValueError:
            raise AuthenticationFailed("Invalid token or token does not exist.")
        
        try:
            # Retrieve form data
            description = request.POST.get('description')
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')
            photo = request.FILES.get('photo')  # Optional field

            # Check required fields
            required_fields = {'description': description, 'longitude': longitude, 'latitude': latitude}
            validate_required_fields(required_fields)

            # Initialize the proof instance (only if a photo is provided)
            proof_instance = None
            if photo:
                photo_url = save_uploaded_file(photo)  # Save the photo and get its URL
                proof_instance = Proof.objects.create(photo=photo_url, creation_date=now())

            # Create the report
            report = Report.objects.create(
                description=description,
                longitude=longitude,
                latitude=latitude,
                user_id=user_id,
                isresolved=0,
                creation_date=now(),  # Set creation_date to the current date and time
                photo=proof_instance  # Optional proof instance
            )

            return JsonResponse({'message': 'Report added successfully', 'report_id': report.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# New method to retrieve reports
@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a list of reports, optionally filtered by user ID.",
    responses={  # Define success and error responses
        200: openapi.Response(description="Reports retrieved successfully."),
        400: openapi.Response(description="Bad request."),
        500: openapi.Response(description="Internal server error."),
    }
)
@api_view(['GET'])
def get_reports(request):
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
        except ValueError:
            raise AuthenticationFailed("Invalid token or token does not exist.")
        
        # Retrieve reports
        reports = Report.objects.filter(isresolved=0)

        # Prepare the response data
        report_data = []
        for report in reports:
            image_path = (
                os.path.join(settings.MEDIA_ROOT, report.photo.photo)
                if report.photo
                else None
            )
            encoded_image = None
            if image_path and os.path.isfile(image_path):
                try:
                    with open(image_path, "rb") as image_file:
                        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                except FileNotFoundError:
                    encoded_image = None
            
            print(report.creation_date)
                
            report_data.append({
                'id': report.id,
                'description': report.description,
                'longitude': report.longitude,
                'latitude': report.latitude,
                'user_id': report.user_id,
                'created_at': report.creation_date,
                'isResolved' : report.isresolved,
                "photo_data": f"data:image/png;base64,{encoded_image}" if encoded_image else None,
            })

        # Return the reports in a JSON response
        return JsonResponse({'reports': report_data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def resolve_report(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            report_id = data.get('report_id')

            token_value = request.headers.get('Authorization')
        
            if not token_value:
                raise AuthenticationFailed("Token is missing in the request.")
            
            user_id = None
    
            refresh_token = RefreshToken(token_value)
            user_id = refresh_token['user_id']
            
            report = Report.objects.get(pk=report_id)
            report.isresolved=1
            report.save()

            # Sauvegarder le signalement comme résolu
            ReportResolved.objects.create(
                user_id=user_id,
                resolved_at=datetime.now(),
                report=report
            )
            
            return JsonResponse({"message": "Signalement marqué comme résolu."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
