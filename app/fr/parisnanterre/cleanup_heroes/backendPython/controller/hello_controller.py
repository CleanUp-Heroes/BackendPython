# hello_controller.py
from django.http import HttpResponse

def hello_view(request):
    return HttpResponse("Hello from API", content_type="text/plain")
