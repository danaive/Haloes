from django.db import models
from person.models import Person
from challenge.models import Challenge
from contest.models import Contest

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    leader = models.OneToOneField(Person, related_name='led_team')
    score = models.PositiveIntegerField(default=0)
    avatar = models.FilePathField()
    solved = models.ManyToManyField(Challenge)
    pwn_list = models.ManyToManyField(Challenge, related_name='+')
    reverse_list = models.ManyToManyField(Challenge, related_name='+')
    web_list = models.ManyToManyField(Challenge, related_name='+')
    crypto_list = models.ManyToManyField(Challenge, related_name='+')
    misc_list = models.ManyToManyField(Challenge, related_name='+')
    ranks = models.ManyToManyField(Contest, through='Ranking')


class Ranking(models.Model):
    team = models.ForeignKey(Team)
    contest = models.ForeignKey(Contest)
    ranking = models.PositiveIntegerField()