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
    """Enregistrer un fichier uploadé dans le dossier MEDIA_ROOT avec un nom unique, en vérifiant l'unicité en base de données."""
    original_name = file.name
    unique_name = generate_unique_filename(original_name)

    # Vérifier que le nom est unique en base de données
    while Proof.objects.filter(photo=unique_name).exists():  # Vérifier si le fichier existe déjà dans la BDD
        unique_name = generate_unique_filename(original_name)  # Si oui, générer un autre nom unique

    # Construire le chemin complet du fichier dans MEDIA_ROOT
    file_path = os.path.join(settings.MEDIA_ROOT, 'proof_photos', unique_name)

    # Normaliser le chemin pour éviter des problèmes avec les séparateurs
    file_path = os.path.normpath(file_path)

    # Sauvegarder le fichier avec un nom unique dans le répertoire MEDIA_ROOT
    default_storage.save(file_path, ContentFile(file.read()))

    # Retourner l'URL d'accès au fichier, avec un séparateur cohérent
    return os.path.join(settings.MEDIA_ROOT, 'proof_photos', unique_name).replace(os.sep, '/')

def validate_required_fields(required_fields):
    """Vérifier que tous les champs requis sont fournis et non vides."""
    missing_fields = [field for field, value in required_fields.items() if not value]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

def handle_error(exception):
    """Gérer les erreurs et retourner une réponse JSON appropriée."""
    return JsonResponse({'error': str(exception)}, status=500)
