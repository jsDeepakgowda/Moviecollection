from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genres = models.CharField(max_length=100)
    uuid = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, related_name='movies', on_delete=models.CASCADE)
