from django.db import models

class Contest(models.Model):
    title = models.CharField(max_length=50, unique=True)
    start_time = models.DateTimeField()
    length = models.DurationField()
    registered = models.ManyToManyField('team.Team')
