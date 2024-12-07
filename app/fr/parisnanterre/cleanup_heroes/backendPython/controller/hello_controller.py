# hello_controller.py
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view


@swagger_auto_schema(
    method='get',
    operation_description="Obtenez un message de salutation",
    responses={200: openapi.Response(description="Plain text response containing 'Hello API'")}
)
@api_view(['GET'])
def hello_api(request):
    return HttpResponse("Hello API", content_type="text/plain")
