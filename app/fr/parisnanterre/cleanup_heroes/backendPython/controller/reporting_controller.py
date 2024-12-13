from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view
from app.models import Report, Proof
from app.fr.parisnanterre.cleanup_heroes.backendPython.utils.utils import save_uploaded_file, validate_required_fields
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Swagger documentation for the POST method
@swagger_auto_schema(
    method='post',
    operation_description="Create a report by submitting a description, address, photo (file), and user ID.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['description', 'adresse', 'user_id', 'photo'],
        properties={
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="The description of the report."),
            'adresse': openapi.Schema(type=openapi.TYPE_STRING, description="The address where the report was made."),
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the user submitting the report."),
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
        try:
            # Retrieve form data
            description = request.POST.get('description')
            adresse = request.POST.get('adresse')
            user_id = request.POST.get('user_id')
            photo = request.FILES.get('photo')

            # Check required fields
            required_fields = {'description': description, 'adresse': adresse, 'user_id': user_id, 'photo': photo}
            validate_required_fields(required_fields)

            # Save the uploaded photo in the 'reports_photos/' directory with a unique name
            photo_url = save_uploaded_file(photo)  # The photo is saved and a unique URL is returned

            # Create a Proof instance and associate it with the photo
            proof_instance = Proof.objects.create(photo=photo_url)

            # Create the report and associate the Proof instance with the photo field
            report = Report.objects.create(
                description=description,
                location=adresse,
                user_id=user_id,
                photo=proof_instance,  # Associating the Proof instance
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
        # Get the 'user_id' parameter from the request (optional)
        user_id = request.GET.get('user_id')

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
