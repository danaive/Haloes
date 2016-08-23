# -*- coding: utf-8 -*-
from django.db import models


class Contest(models.Model):
    title = models.CharField(max_length=50, unique=True)
    time = models.DateTimeField()
    length = models.DurationField()
    registered = models.ManyToManyField('person.Person')
