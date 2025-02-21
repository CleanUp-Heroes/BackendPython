# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime
from django.utils.timezone import now # ajouter par claire sur la fonction creation date pour run le back

from django.core.validators import RegexValidator # ajout par claire la validation du numéro de téléphone


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    expected_actions = models.IntegerField()
    unit = models.ForeignKey('Unit', models.DO_NOTHING)
    points = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'challenge'


class CompletedChallenge(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    challenge = models.ForeignKey(Challenge, models.DO_NOTHING)
    completion_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'completed_challenge'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Participation(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    challenge = models.ForeignKey(Challenge, models.DO_NOTHING)
    action_quantity = models.FloatField()
    action_date = models.DateField()
    photo = models.ForeignKey('Proof', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'participation'


class Proof(models.Model):
    photo = models.CharField(max_length=255)
    creation_date = models.DateTimeField(datetime.now()) 
    


    class Meta:
        managed = False
        db_table = 'proof'


class Report(models.Model):
    description = models.TextField()
    location = models.CharField(max_length=255)
    photo = models.ForeignKey(Proof, models.DO_NOTHING, blank=True, null=True)
    #creation_date = models.DateField(default=datetime.now())problème lors du run du back, donc
    creation_date = models.DateTimeField(default=now)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'report'


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class Unit(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'unit'



# La base de données pour le feature vontariat

# formation
class Formation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

from django.db import models

# Création de mission
class Mission(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    localisation = models.CharField(max_length=100)
    type_pollution = models.CharField(max_length=50)
    difficulte = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return self.titre
    
    # migration qui a été fait  : Cela vous indique que Django a créé un nouveau fichier de migration 
    # dans le répertoire app\migrations.
    #  Ce fichier porte le nom 0003_alter_mission_difficulte_alter_mission_localisation_and_more.py.
    

class Candidature(models.Model):
    STATUS_CHOICES = [
        ('en attente', 'En attente'),
        ('acceptée', 'Acceptée'),
        ('refusée', 'Refusée'),
    ]

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format : '+999999999'."
    )

    name = models.CharField(max_length=255, verbose_name="Nom du volontaire")
    email = models.EmailField(verbose_name="Email du volontaire")
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name="Téléphone du volontaire")
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, verbose_name="Mission")
    message = models.TextField(verbose_name="Message du volontaire", blank=True, null=True)
    experience = models.TextField(verbose_name="Expérience du volontaire", blank=True, null=True)
    availability = models.CharField(max_length=255, verbose_name="Disponibilités du volontaire")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en attente', verbose_name="Statut")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Candidature de {self.name} pour {self.mission.titre}"

    class Meta:
        db_table = 'candidature'  # Nom de la table dans la base de données