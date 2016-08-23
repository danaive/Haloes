# -*- coding: utf-8 -*-
from django.db import models
from challenge.models import Challenge
from person.models import Person


class Writeup(models.Model):
    author = models.ForeignKey(Person)
    challenge = models.ForeignKey(Challenge)
    comments = models.ManyToManyField(Person, related_name='+', through='Comment', through_fields=('writeup', 'author'))
    likes = models.ManyToManyField(Person, related_name='likes')
    stars = models.ManyToManyField(Person, related_name='stars')
    content = models.TextField()
    title = models.CharField(max_length=50)
    time = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title + '@' + self.author.username


class Comment(models.Model):
    author = models.ForeignKey(Person, related_name='comments')
    writeup = models.ForeignKey(Writeup)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(Person, related_name='replies', null=True)
