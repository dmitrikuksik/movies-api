from django.db import models
from django.contrib.postgres.fields import JSONField

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    data = JSONField()


