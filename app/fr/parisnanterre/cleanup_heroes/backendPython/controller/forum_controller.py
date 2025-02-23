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
    ForumCategories,
    ForumModerationAction,
)

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
            category_id = data.get("category")
            
            if not title or not content or not category_id:
                return JsonResponse({"error": "Tous les champs sont requis"}, status=400)
            
            try:
                category = ForumCategories.objects.get(id=category_id)
            except ForumCategories.DoesNotExist:
                return JsonResponse({"error": "Catégorie non trouvée"}, status=400)
            
            # Créer le sujet
            sujet = ForumSujets.objects.create(
                title=title,
                content=content,
                user=user,
                category="category",
                created_at=now()
            )
            
            return JsonResponse({
                "message": "Sujet créé avec succès",
                "sujet": {
                    "id": sujet.id,
                    "title": sujet.title,
                    "content": sujet.content,
                    "created_at": sujet.created_at,
                    "category": sujet.category.name,
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
    category_id = request.GET.get('category', None)
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
        'category': topic.category.name,
        'like_count': topic.like_count,
        'reply_count': topic.reply_count
    } for topic in topics]

    return JsonResponse({'topics': topics_data}, status=200)


def get_forum_categories(request):
    """
    Récupère la liste des catégories de sujets du forum.
    """
    categories = ForumCategories.objects.all().values('id', 'name')
    return JsonResponse({'categories': list(categories)}, status=200)

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
    content = request.POST.get('reply')
    if not content:
        return JsonResponse({'error': 'Le contenu ne peut pas être vide.'}, status=400)
    
    token_value = request.headers.get('Authorization')
    topic = get_object_or_404(ForumSujets, id=topic_id)
    refresh_token = RefreshToken(token_value)
    user_id = refresh_token['user_id']
    user = AuthUser.objects.get(id=user_id)
    reply = ForumReponses.objects.create(sujet=topic, user=user, content=content)

    return JsonResponse({'message': 'Réponse ajoutée avec succès.', 'reply_id': reply.id}, status=201)

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

    # Récupération des signalements de sujets non traités
    subject_reports = ForumSignalementsSujet.objects.select_related("user", "sujet").filter(is_handled=False).order_by("-created_at")
    subject_reports_data = [{
        "id": report.id,
        "type": "sujet",
        "user": report.user.username,
        "sujet_id": report.sujet.id if report.sujet else None,
        "sujet_title": report.sujet.title if report.sujet else None,
        "reason": report.reason,
        "created_at": report.created_at,
    } for report in subject_reports]

    # Récupération des signalements de réponses non traités
    response_reports = ForumSignalementsReponse.objects.select_related("user", "reponse", "sujet").filter(is_handled=False).order_by("-created_at")
    response_reports_data = [{
        "id": report.id,
        "type": "réponse",
        "user": report.user.username,
        "sujet_id": report.sujet.id if report.sujet else None,
        "sujet_title": report.sujet.title if report.sujet else None,
        "reponse_id": report.reponse.id if report.reponse else None,
        "reponse_content": report.reponse.content if report.reponse else None,
        "reason": report.reason,
        "created_at": report.created_at,
    } for report in response_reports]

    # Fusionner les résultats
    all_reports = subject_reports_data + response_reports_data
    all_reports = sorted(all_reports, key=lambda x: x["created_at"], reverse=True)  # Trier par date

    return JsonResponse({"reports": all_reports}, status=200, safe=False)


# @csrf_exempt
def list_reported_content(request):
    if request.method == 'GET':
        try:
            # Récupérer les signalements de sujets
            reported_sujets = ForumSignalementsSujet.objects.all()
            sujets_data = []
            for report in reported_sujets:
                sujets_data.append({
                    'report_id': report.id,
                    'type': 'sujet',
                    'user_id': report.user.id,
                    'sujet_id': report.sujet.id if report.sujet else None,
                    'reason': report.reason,
                    'created_at': report.created_at.isoformat() if report.created_at else None,
                })
            # Récupérer les signalements de réponses
            reported_reponses = ForumSignalementsReponse.objects.all()
            reponses_data = []
            for report in reported_reponses:
                reponses_data.append({
                    'report_id': report.id,
                    'type': 'reponse',
                    'user_id': report.user.id,
                    'sujet_id': report.sujet.id if report.sujet else None,
                    'reponse_id': report.reponse.id if report.reponse else None,
                    'reason': report.reason,
                    'created_at': report.created_at.isoformat() if report.created_at else None,
                })
            # Combiner et trier par date (optionnel)
            all_reports = sujets_data + reponses_data
            all_reports.sort(key=lambda x: x['created_at'] or '', reverse=True)
            return JsonResponse({'reports': all_reports}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
 
@csrf_exempt
def moderate_report(request, report_id):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        
        # Récupérer le rapport
        report = ForumSignalementsSujet.objects.filter(id=report_id).first() or \
                ForumSignalementsReponse.objects.filter(id=report_id).first()

        if not report:
            return JsonResponse({"error": "Signalement non trouvé"}, status=400)

        # Action : Édition ou suppression
        if action == "edite":
            if isinstance(report, ForumSignalementsSujet):
                report.sujet.content = data.get("new_content", report.sujet.content)
                report.sujet.save()
            elif isinstance(report, ForumSignalementsReponse):
                report.reponse.content = data.get("new_content", report.reponse.content)
                report.reponse.save()

            # Marquer le signalement comme traité
            report.is_handled = True
            report.save()

            return JsonResponse({"message": "Contenu édité avec succès et signalement traité"}, status=200)
        
        elif action == "supprime":
            if isinstance(report, ForumSignalementsSujet):
                report.sujet.is_deleted = True
                report.sujet.save()
            elif isinstance(report, ForumSignalementsReponse):
                report.reponse.is_deleted = True
                report.reponse.save()

            # Marquer le signalement comme traité
            report.is_handled = True
            report.save()

            return JsonResponse({"message": "Contenu supprimé avec succès et signalement traité"}, status=200)
        
        return JsonResponse({"error": "Action non reconnue"}, status=400)
