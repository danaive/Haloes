from django.db import models
from challenge.models import Challenge
from person.models import Person


class Writeup(models.Model):
    author = models.ForeignKey(Person)
    challenge = models.ForeignKey(Challenge)
    comments = models.ManyToManyField(Person, related_name='+', through='Comment')
    likes = models.ManyToManyField(Person, related_name='likes')
    content = models.FilePathField()


class Comment(models.Model):
    author = models.ForeignKey(Person)
    writeup = models.ForeignKey(Writeup)
    content = models.TextField()
