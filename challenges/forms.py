# formulaire pour un defis
# challenges/forms.py

from django import forms
from .models import Challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['name', 'description', 'start_date', 'end_date']
