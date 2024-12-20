from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view
from app.models import Report, Proof
from app.fr.parisnanterre.cleanup_heroes.backendPython.utils.utils import save_uploaded_file, validate_required_fields
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.utils.timezone import now

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
            adresse = request.POST.get('location')
            photo = request.FILES.get('photo')  # Optional field

            # Check required fields
            required_fields = {'description': description, 'adresse': adresse}
            validate_required_fields(required_fields)

            # Initialize the proof instance (only if a photo is provided)
            proof_instance = None
            if photo:
                photo_url = save_uploaded_file(photo)  # Save the photo and get its URL
                proof_instance = Proof.objects.create(photo=photo_url)

            # Create the report
            report = Report.objects.create(
                description=description,
                location=adresse,
                user_id=user_id,
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
        
        # Retrieve reports based on the filter
        if user_id:
            reports = Report.objects.filter(user_id=user_id)
        else:
            reports = Report.objects.all()

        # Prepare the response data
        report_data = []
        for report in reports:
            report_data.append({
                'id': report.id,
                'description': report.description,
                'location': report.location,
                'user_id': report.user_id,
                'photo_url': report.photo.photo,  # The URL of the photo is stored in the Proof model
            })

        # Return the reports in a JSON response
        return JsonResponse({'reports': report_data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
