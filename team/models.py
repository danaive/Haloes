# -*- coding: utf-8 -*-
from django.db import models
from person.models import Person, Submit
from challenge.models import Challenge
from contest.models import Contest


def upload_to_team(instance, filename):
    from os import urandom
    return 'avatar/team/%s.%s.png' % (instance.name, urandom(4).encode('hex'))


def upload_to_group(instance, filename):
    from os import urandom
    return 'avatar/group/%s.%s.png' % (instance.name, urandom(4).encode('hex'))


class Team(models.Model):
    name = models.CharField(max_length=50)
    leader = models.OneToOneField(Person, related_name='led_team')
    member = models.ManyToManyField(Person, related_name='teams')
    score = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=upload_to_team)
    solved = models.ManyToManyField(Challenge)
    ranks = models.ManyToManyField(Contest, through='Ranking')
    code = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    leader = models.OneToOneField(Person, related_name='led_group')
    score = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=upload_to_group, default='avatar/group/default.gif')
    solved = models.ManyToManyField(Challenge)
    code = models.CharField(max_length=50)

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
    datetime = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True)
    content = models.CharField(max_length=100)
    assign_to = models.ForeignKey(Person, null=True, related_name='assigned_tasks')
    done = models.BooleanField(default=False)
    checker = models.ForeignKey(Person, null=True)


class Issue(models.Model):
    author = models.ForeignKey(Person)
    group = models.ForeignKey(Group, related_name='issues')
    comments = models.ManyToManyField(Person, related_name='+', through='Comment', through_fields=('issue', 'author'))
    content = models.TextField()
    title = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(Person, related_name='issue_comments')
    issue = models.ForeignKey(Issue)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(Person, related_name='issue_replies', null=True)


class GroupMaxScore(models.Model):
    category = models.CharField(max_length=10)
    score = models.PositiveIntegerField(default=0)


def recalc_score(group):
    group.solved.clear()
    for user in group.members.all():
        for challenge in user.challenges.filter(submit__status=True):
            group.solved.add(challenge)
    score = [0, 0, 0, 0, 0]
    cate = {'PWN': 0, 'REVERSE': 1, 'WEB': 2, 'CRYPTO': 3, 'MISC': 4}
    group.score = 0
    for challenge in group.solved.all():
        group.score += challenge.score
        score[cate[challenge.category]] += challenge.score
    group.save()
    for key in cate:
        gms = GroupMaxScore.objects.get(category=key)
        if score[cate[key]] > gms.score:
            gms.score = score[cate[key]]
            gms.save()
