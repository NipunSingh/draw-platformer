from __future__ import unicode_literals

from django.db import models

# Create your models here.

class GameMap(models.Model):
    title = models.CharField(max_length=200)
    map = models.TextField()
    high_score = models.IntegerField(default=9999)
    created = models.DateTimeField(auto_now_add=True, null=True)
