from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.utils import timezone
from app.models import (
    ForumSignalementsReponse, 
    ForumSignalementsSujet, 
    ForumSujets, 
    ForumReponses, 
    AuthUser,
    ForumSujetsVotes,
    ForumModerationAction,
)

@csrf_exempt
def update_sujet(request, sujet_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        sujet = get_object_or_404(ForumSujets, id=sujet_id)

        titre = data.get("titre")
        contenu = data.get("contenu")
        # Mise à jour du sujet
        # sujet.title = titre
        # sujet.content = contenu
        # sujet.save()

        return JsonResponse({"message": "Sujet mis à jour avec succès", "sujet": {
            "id": sujet.id,
            "titre": sujet.title,
            "contenu": sujet.content
        }})

@csrf_exempt
def delete_sujet(request, sujet_id):
    if request.method == "DELETE":
        sujet = get_object_or_404(ForumSujets, id=sujet_id)
        sujet.delete()
        return JsonResponse({"message": "Sujet supprimé avec succès"})

@csrf_exempt
def update_reponse(request, reponse_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        reponse = get_object_or_404(ForumReponses, id=reponse_id)

        # Mise à jour de la réponse
        reponse.content = data.get("contenu", reponse.content)
        reponse.save()

        return JsonResponse({"message": "Réponse mise à jour avec succès", "reponse": {
            "id": reponse.id,
            "contenu": reponse.content
        }})

@csrf_exempt
def delete_reponse(request, reponse_id):
    if request.method == "DELETE":
        reponse = get_object_or_404(ForumReponses, id=reponse_id)          

        reponse.delete()
        return JsonResponse({"message": "Réponse supprimée avec succès"})

@csrf_exempt
def create_topic(request):
    try:
        token_value = request.headers.get('Authorization')

        if not token_value:
            raise AuthenticationFailed("Token is missing in the request.")
        
        user_id = None
        try:
            refresh_token = RefreshToken(token_value)
            user_id = refresh_token['user_id']

            user = AuthUser.objects.get(id=user_id)

            if not user.is_active:
                raise AuthenticationFailed('User is inactive.')
        except ValueError:
            raise AuthenticationFailed("Invalid token or token does not exist.")
        
        # Vérifier si la méthode est POST
        if request.method == "POST":
            data = json.loads(request.body)
            
            title = data.get("title")
            content = data.get("content")
            
            if not title or not content :
                return JsonResponse({"error": "Tous les champs sont requis"}, status=400)
            
          
            # Créer le sujet
            sujet = ForumSujets.objects.create(
                title=title,
                content=content,
                user=user,
                created_at=now(),
                is_deleted=0,
                status='actif'
            )
            
            return JsonResponse({
                "message": "Sujet créé avec succès",
                "sujet": {
                    "id": sujet.id,
                    "title": sujet.title,
                    "content": sujet.content,
                    "created_at": sujet.created_at,
                    "user": user.username,
                }
            }, status=201)

        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
def like_topic(request, topic_id):
    try:
        token_value = request.headers.get('Authorization')
        if not token_value:
            raise AuthenticationFailed("Token is missing in the request.")

        try:
            refresh_token = RefreshToken(token_value)
            user_id = refresh_token['user_id']
            user = AuthUser.objects.get(id=user_id)

            if not user.is_active:
                raise AuthenticationFailed('User is inactive.')
        except ValueError:
            raise AuthenticationFailed("Invalid token or token does not exist.")

        topic = get_object_or_404(ForumSujets, id=topic_id)
        
        like, created = ForumSujetsVotes.objects.get_or_create(user=user, sujet=topic)

        if not created:
            like.delete()  # Si un like existait déjà, on l'annule
            message = "Like supprimé"
        else:
            message = "Like ajouté"

        like_count = ForumSujetsVotes.objects.filter(sujet=topic).count()

        return JsonResponse({"message": message, "like_count": like_count}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def get_forum_topics(request):
    """
    Récupère la liste des sujets du forum avec possibilité de filtrer par catégorie,
    de trier par date ou popularité, et d'inclure le nombre de votes et de réponses.
    """
    # sort_by = request.GET.get('sort_by', 'date')  # 'date' (par défaut) ou 'popularité'
    
    topics = ForumSujets.objects.filter(is_deleted=False).annotate(
        like_count=Count('forumsujetsvotes__id', distinct=True),
        reply_count=Count('forumreponses__id', distinct=True)
    )

    # if category_id:
    #     topics = topics.filter(category_id=category_id)

    # if sort_by == 'popularité':
    #     topics = topics.order_by('-like_count', '-created_at')  # Popularité puis date en cas d'égalité
    # else:
    #     topics = topics.order_by('-created_at')

    topics_data = [{
        'id': topic.id,
        'title': topic.title,
        'author': topic.user.username,
        'created_at': topic.created_at,
        'like_count': topic.like_count,
        'reply_count': topic.reply_count
    } for topic in topics]

    return JsonResponse({'topics': topics_data}, status=200)


# def get_forum_categories(request):
#     """
#     Récupère la liste des catégories de sujets du forum.
#     """
#     categories = ForumCategories.objects.all().values('id', 'name')
#     return JsonResponse({'categories': list(categories)}, status=200)

def vote_forum_topic(request, topic_id):
    """
    Permet à un utilisateur connecté de voter pour un sujet.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Vous devez être connecté pour voter.'}, status=401)

    try:
        topic = get_object_or_404(ForumSujets, id=topic_id)

       

        existing_vote = ForumSujetsVotes.objects.filter(user=request.user, sujet=topic).first()
        if existing_vote:
            existing_vote.save()
        else:
            ForumSujetsVotes.objects.create(user=request.user, sujet=topic)

        return JsonResponse({'message': 'Vote enregistré avec succès.'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Sujet non trouvé.'}, status=404)
    
def get_topic_detail(request, topic_id):
    topic = get_object_or_404(ForumSujets, id=topic_id)
    
    # Nombre total de likes
    like_count = ForumSujetsVotes.objects.filter(sujet=topic).count()
    
    token_value = request.headers.get('Authorization')
    refresh_token = RefreshToken(token_value)
    user_id = refresh_token['user_id']
    user = AuthUser.objects.get(id=user_id)

    # Vérifier si l'utilisateur a liké
    user_has_liked = ForumSujetsVotes.objects.filter(sujet=topic, user=user).exists()

    topic_data = {
        'id': topic.id,
        'title': topic.title,
        'content': topic.content,
        'author': topic.user.username,
        'created_at': topic.created_at,
        'like_count': like_count,
        'user_has_liked': user_has_liked,
    }
    
    # Récupérer les réponses non supprimées
    replies = ForumReponses.objects.filter(sujet_id=topic_id, is_deleted=False).order_by('created_at')
    replies_data = [{
        'id': reply.id,
        'content': reply.content,
        'author': reply.user.username,
        'created_at': reply.created_at,
    } for reply in replies]
    
    topic_data['replies'] = replies_data
    
    return JsonResponse(topic_data, status=200)

def get_topic_replies(request, topic_id):
    """
    Récupère les réponses associées à un sujet du forum.
    """
    replies = ForumReponses.objects.filter(sujet_id=topic_id).order_by('created_at')
    replies_data = [{
        'id': reply.id,
        'content': reply.content,
        'author': reply.user.username,
        'created_at': reply.created_at,
    } for reply in replies]
    
    return JsonResponse({'replies': replies_data}, status=200)


@csrf_exempt
def add_reply(request, topic_id):
    """
    Ajoute une réponse à un sujet du forum (nécessite une authentification).
    """
    if request.method != "POST":
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    try:
        data = json.loads(request.body)  # Récupérer le JSON envoyé
        content = data.get('reply')

        if not content or not content.strip():
            return JsonResponse({'error': 'Le contenu ne peut pas être vide.'}, status=400)
        
        token_value = request.headers.get('Authorization')
        if not token_value:
            return JsonResponse({'error': 'Token manquant'}, status=401)

        refresh_token = RefreshToken(token_value)
        user_id = refresh_token['user_id']
        user = AuthUser.objects.get(id=user_id)

        topic = get_object_or_404(ForumSujets, id=topic_id)
        reply = ForumReponses.objects.create(sujet=topic, user=user, content=content, is_deleted=0)

        return JsonResponse({'message': 'Réponse ajoutée avec succès.', 'reply_id': reply.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données invalides, format JSON attendu.'}, status=400)
    except AuthUser.DoesNotExist:
        return JsonResponse({'error': 'Utilisateur non trouvé.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Erreur interne : {str(e)}'}, status=500)

@csrf_exempt
def report_subject(request):
    """
    Endpoint pour signaler un sujet inapproprié.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        token_value = request.headers.get('Authorization')
        refresh_token = RefreshToken(token_value)
        user_id = refresh_token['user_id']
        user = AuthUser.objects.get(id=user_id)

        data = json.loads(request.body)
        reason = data.get("reason", "").strip()
        sujet_id = data.get("sujet_id")

        if not reason:
            return JsonResponse({"error": "La raison du signalement est obligatoire"}, status=400)

        sujet = ForumSujets.objects.filter(id=sujet_id).first()
        if not sujet:
            return JsonResponse({"error": "Sujet introuvable"}, status=400)

        # Création du signalement
        ForumSignalementsSujet.objects.create(
            user=user,
            sujet=sujet,
            reason=reason,
            created_at=timezone.now()
        )

        return JsonResponse({"message": "Signalement du sujet enregistré"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Format JSON invalide"}, status=400)

@csrf_exempt
def report_response(request):
    """
    Endpoint pour signaler une réponse inappropriée.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)
        token_value = request.headers.get('Authorization')
        refresh_token = RefreshToken(token_value)
        user_id = refresh_token['user_id']
        user = AuthUser.objects.get(id=user_id)
        reason = data.get("reason", "").strip()
        reponse_id = data.get("sujet_id")

        if not reason:
            return JsonResponse({"error": "La raison du signalement est obligatoire"}, status=400)

        reponse = ForumReponses.objects.filter(id=reponse_id).first()
        if not reponse:
            return JsonResponse({"error": "Réponse introuvable"}, status=404)

        # Création du signalement
        ForumSignalementsReponse.objects.create(
            user=user,
            reponse=reponse,
            sujet=reponse.sujet,  # Associe la réponse à son sujet
            reason=reason,
            created_at=timezone.now()
        )

        return JsonResponse({"message": "Signalement de la réponse enregistré"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Format JSON invalide"}, status=400)

def get_reports(request):
    """
    Endpoint pour récupérer tous les signalements (sujets et réponses).
    Accessible uniquement aux modérateurs.
    """
    if not request.user.forummoderateur_set.exists():  
        return JsonResponse({"error": "Accès interdit"}, status=403)

    # Signalements des sujets
    subject_reports = ForumSignalementsSujet.objects.select_related("user", "sujet", "sujet__user").filter(
        is_handled=False,
        sujet__is_deleted=False
    ).order_by("-created_at")

    subject_reports_data = [{
        "id": report.id,
        "type": "sujet",
        "user": report.user.username,
        "sujet_id": report.sujet.id if report.sujet else None,
        "sujet_title": report.sujet.title if report.sujet else None,
        "sujet_content": report.sujet.content if report.sujet else None,  # Ajout du contenu
        "sujet_author": report.sujet.user.username if report.sujet and report.sujet.user else None,  # Auteur du sujet
        "reason": report.reason,
        "created_at": report.created_at,
    } for report in subject_reports]

    # Signalements des réponses
    response_reports = ForumSignalementsReponse.objects.select_related("user", "reponse", "reponse__user", "sujet").filter(
        is_handled=False,
        sujet__is_deleted=False,
        reponse__is_deleted=False  # Vérifier aussi que la réponse n'est pas supprimée
    ).order_by("-created_at")

    response_reports_data = [{
        "id": report.id,
        "type": "réponse",
        "user": report.user.username,
        "sujet_id": report.sujet.id if report.sujet else None,
        "sujet_title": report.sujet.title if report.sujet else None,
        "reponse_id": report.reponse.id if report.reponse else None,
        "reponse_content": report.reponse.content if report.reponse else None,
        "reponse_author": report.reponse.user.username if report.reponse and report.reponse.user else None,  # Auteur de la réponse
        "reason": report.reason,
        "created_at": report.created_at,
    } for report in response_reports]

    all_reports = sorted(subject_reports_data + response_reports_data, key=lambda x: x["created_at"], reverse=True)

    return JsonResponse({"reports": all_reports}, status=200, safe=False)

# @csrf_exempt
def list_reported_content(request):

    # Signalements des sujets
    subject_reports = ForumSignalementsSujet.objects.select_related("user", "sujet", "sujet__user").filter(
        is_handled=False,
        sujet__is_deleted=False
    ).order_by("-created_at")

    subject_reports_data = [{
        "id": report.id,
        "type": "sujet",
        "user": report.user.username,
        "sujet_id": report.sujet.id if report.sujet else None,
        "sujet_title": report.sujet.title if report.sujet else None,
        "sujet_content": report.sujet.content if report.sujet else None,  # Ajout du contenu
        "sujet_author": report.sujet.user.username if report.sujet and report.sujet.user else None,  # Auteur du sujet
        "reason": report.reason,
        "created_at": report.created_at,
    } for report in subject_reports]

    # Signalements des réponses
    response_reports = ForumSignalementsReponse.objects.select_related("user", "reponse", "reponse__user", "sujet").filter(
        is_handled=False,
        sujet__is_deleted=False,
        reponse__is_deleted=False  # Vérifier aussi que la réponse n'est pas supprimée
    ).order_by("-created_at")

    response_reports_data = [{
        "id": report.id,
        "type": "réponse",
        "user": report.user.username,
        "sujet_id": report.sujet.id if report.sujet else None,
        "sujet_title": report.sujet.title if report.sujet else None,
        "reponse_id": report.reponse.id if report.reponse else None,
        "reponse_content": report.reponse.content if report.reponse else None,
        "reponse_author": report.reponse.user.username if report.reponse and report.reponse.user else None,  # Auteur de la réponse
        "reason": report.reason,
        "created_at": report.created_at,
    } for report in response_reports]

    all_reports = sorted(subject_reports_data + response_reports_data, key=lambda x: x["created_at"], reverse=True)

    return JsonResponse({"reports": all_reports}, status=200, safe=False)

@csrf_exempt
@login_required
def moderation_action(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)
        moderator = request.user
        report_id = data.get("report_id")
        report_type = data.get("type")  # 'sujet' ou 'réponse'
        action = data.get("action")
        comment = data.get("comment", "")

        if not report_id or not action:
            return JsonResponse({"error": "Données manquantes"}, status=400)

        # Déterminer si c'est un signalement de sujet ou de réponse
        forum_signalements_sujet = None
        forum_signalements_reponse = None

        if report_type == "sujet":
            try:
                forum_signalements_sujet = ForumSignalementsSujet.objects.get(id=report_id)
            except ForumSignalementsSujet.DoesNotExist:
                return JsonResponse({"error": "Signalement de sujet introuvable"}, status=404)
        
        elif report_type == "réponse":
            try:
                forum_signalements_reponse = ForumSignalementsReponse.objects.get(id=report_id)
            except ForumSignalementsReponse.DoesNotExist:
                return JsonResponse({"error": "Signalement de réponse introuvable"}, status=404)
        
        else:
            return JsonResponse({"error": "Type de signalement invalide"}, status=400)

        # Enregistrer l'action de modération
        moderation_action = ForumModerationAction.objects.create(
            moderator=moderator,
            forum_signalements_sujet=forum_signalements_sujet,
            forum_signalements_reponse=forum_signalements_reponse,
            action=action,
            comment=comment,
            created_at=datetime.now(),
        )

        return JsonResponse({"message": "Action de modération enregistrée avec succès", "action_id": moderation_action.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Format JSON invalide"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
