from django.db import models
from django.contrib.postgres.fields import JSONField

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    data = JSONField()

class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()


