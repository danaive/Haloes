from django.db import models

class Challenge(models.Model):
    title = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=10)
    flag = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    solved = models.PositiveIntegerField(default=0)
