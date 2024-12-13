# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    expected_actions = models.IntegerField()
    unit = models.ForeignKey('Unit', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'challenge'


class CompletedChallenge(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    challenge = models.ForeignKey(Challenge, models.DO_NOTHING)
    completion_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'completed_challenge'


class Participation(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    challenge = models.ForeignKey(Challenge, models.DO_NOTHING)
    action_quantity = models.FloatField()
    action_date = models.DateField()
    photo = models.ForeignKey('Proof', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'participation'


class Proof(models.Model):
    photo = models.CharField(max_length=255)
    creation_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'proof'


class Report(models.Model):
    description = models.TextField()
    location = models.CharField(max_length=255)
    photo = models.ForeignKey(Proof, models.DO_NOTHING, blank=True, null=True)
    creation_date = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'report'


class Unit(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'unit'


class User(models.Model):
    name = models.CharField(unique=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'user'