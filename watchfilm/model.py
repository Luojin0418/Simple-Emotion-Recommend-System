# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from djongo import models


class Film(models.Model):
    _id = models.TextField(primary_key=True)  # This field type is a guess.
    rating = models.CharField(max_length=5)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    describe = models.CharField(max_length=100)
    short_comment = models.CharField(max_length=500)
    image_url = models.CharField(max_length=100)

    actor = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'film'


class kmean_recom(models.Model):
    _id = models.TextField(primary_key=True)  # This field type is a guess.
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=5)

    class Meta:
        managed = True
        db_table = 'kmeans'


class user(models.Model):
    _id = models.TextField(primary_key=True)
    title = models.CharField(max_length=10)
    happy = models.CharField(max_length=50)
    neutral = models.CharField(max_length=50)
    disgust = models.CharField(max_length=50)
    angry = models.CharField(max_length=50)
    surprise = models.CharField(max_length=50)
    sad = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = 'user'