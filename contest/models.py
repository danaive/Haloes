from django.db import models
from team.models import Team

class Contest(models.Model):
    title = models.CharField(max_length=50, unique=True)
    start_time = models.DateTimeField()
    length = models.DurationField()
    registered = models.ManyToManyField(Team)
