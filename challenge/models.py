from django.db import models
from contest.models import Contest

class Challenge(models.Model):
    title = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=10)
    flag = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    solved = models.PositiveIntegerField(default=0)
    contest = models.ForeignKey(Contest, null=True, blank=True, on_delete=models.SET_NULL)
    url = models.URLField()