from __future__ import unicode_literals
from django.db import models

# Create your models here.

class GameMap(models.Model):
    title = models.CharField(max_length=200)
    map = models.TextField()
    high_score = models.IntegerField(default=9999)
    high_score_name = models.CharField(max_length=20, default="Anonymous")
    created = models.DateTimeField(auto_now_add=True, null=True)
    votes = models.IntegerField(default=1)
    input_img = models.ImageField(upload_to='pics/', default='pics/no-img.jpg')
