# challenges/views.py
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse  # Ajout de l'import pour HttpResponse
from .models import Challenge
from .forms import ChallengeForm

# Vue pour la création de défi (avec un formulaire)
class ChallengeCreateView(CreateView):
    model = Challenge
    template_name = 'challenges/challenge_form.html'
    fields = ['name', 'description', 'start_date', 'end_date']

# Vue pour afficher les statistiques des défis
class ChallengeStatsView(TemplateView):
    template_name = 'challenges/challenge_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges_count'] = Challenge.objects.count()  # Compter le nombre de défis
        return context

# Vue pour afficher la liste des défis
def challenge_list(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenges/challenge_list.html', {'challenges': challenges})

# Vue pour la page d'accueil
def home(request):
    #return HttpResponse("Bienvenue sur la page d'accueil de l'application!")
    return render(request, 'challenges/home.html')