from django.db import models

# Create your models here.

#Création du modèle pour représenter un défi dans l'application challenges
# après la creationde ce modèle je vais faire ça : 
# python manage.py makemigrations challenges
#python manage.py migrate

# challenges/models.py

from django.db import models

class Challenge(models.Model):
    name = models.CharField(max_length=100, default='Default Name')  # Définir un nom par défaut
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Participation(models.Model):
    user = models.CharField(max_length=100)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    proof = models.ImageField(upload_to='proofs/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
