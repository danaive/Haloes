from django.db import models
from person.models import Person, Submit
from challenge.models import Challenge
from contest.models import Contest

def upload_to():
    return 'wtf'


def upload_to_team(instance, filename):
    return 'avatar/team/' + instance.name + filename.split('.')[-1]


def upload_to_group(instance, filename):
    return 'avatar/group/' + instance.name + filename.split('.')[-1]


class Team(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(Person, related_name='led_team')
    member = models.ManyToManyField(Person, related_name='teams')
    score = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=upload_to_team)
    solved = models.ManyToManyField(Challenge)
    ranks = models.ManyToManyField(Contest, through='Ranking')

    def __unicode__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    leader = models.OneToOneField(Person, related_name='led_group')
    score = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=upload_to_group)
    solved = models.ManyToManyField(Challenge)
    pwn_list = models.ManyToManyField(Challenge, related_name='+')
    reverse_list = models.ManyToManyField(Challenge, related_name='+')
    web_list = models.ManyToManyField(Challenge, related_name='+')
    crypto_list = models.ManyToManyField(Challenge, related_name='+')
    misc_list = models.ManyToManyField(Challenge, related_name='+')

    def __unicode__(self):
        return self.name


class Ranking(models.Model):
    # team ranking in contest
    team = models.ForeignKey(Team)
    contest = models.ForeignKey(Contest)
    ranking = models.IntegerField(default=0)
    solved = models.ManyToManyField(Submit)
    score = models.IntegerField(default=0)


class Task(models.Model):
    group = models.ForeignKey(Group, related_name='tasks')
    datetime = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True)
    content = models.CharField(max_length=100)
    assign_to = models.ForeignKey(Person, related_name='assigned_tasks')
    state = models.BooleanField(default=False)