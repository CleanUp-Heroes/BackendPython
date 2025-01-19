import os
import uuid
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from app.models import Proof  # Assurez-vous que Proof est importé si vous devez vérifier dans la BDD

def generate_unique_filename(filename):
    """Générer un nom de fichier unique basé sur un suffixe UUID."""
    unique_suffix = uuid.uuid4().hex  # UUID sans tirets
    return f"{filename.split('.')[0]}_{unique_suffix}.{filename.split('.')[-1]}"

def save_uploaded_file(file):
    """Enregistre un fichier uploadé dans le dossier MEDIA_ROOT avec un nom unique."""
    original_name = file.name
    unique_name = generate_unique_filename(original_name)

    # Construire le chemin relatif au dossier "proof_photos"
    relative_path = os.path.join('proof_photos', unique_name)

    # Construire le chemin absolu pour l'enregistrement
    absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    # Normaliser le chemin absolu
    absolute_path = os.path.normpath(absolute_path)

    # Sauvegarder le fichier
    default_storage.save(absolute_path, ContentFile(file.read()))

    # Retourner uniquement le chemin relatif pour la base de données
    return relative_path


def validate_required_fields(required_fields):
    """Vérifier que tous les champs requis sont fournis et non vides."""
    missing_fields = [field for field, value in required_fields.items() if not value]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

def handle_error(exception):
    """Gérer les erreurs et retourner une réponse JSON appropriée."""
    return JsonResponse({'error': str(exception)}, status=500)
