from django.shortcuts import render
from  app.fr.parisnanterre.cleanup_heroes.backendPython.controller import challenge_controller, hello_controller
from django.http import JsonResponse
from .models import *
from django.db.models import Sum
from datetime import date