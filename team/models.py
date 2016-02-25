from django.db import models
from person.models import Person

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    captain = models.OneToOneField(Person)