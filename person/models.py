from django.db import models
from challenge.models import Challenge


class Person(models.Model):
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    major = models.CharField(max_length=10, default='')
    score = models.PositiveIntegerField(default=0)
    school = models.CharField(max_length=50, blank=True)
    mail = models.EmailField()
    blog = models.URLField()
    avatar = models.FilePathField()
    follow = models.ManyToManyField('self', symmetrical=False)
    solved = models.ManyToManyField(Challenge, through='Submit')
    #attampt = models.ManyToManyField(Challenge, through='Submit')
    #team = models.ForeignKey('Team')


class Submit(models.Model):
    person = models.ForeignKey(Person)
    challenge = models.ForeignKey(Challenge)
    date = models.DateTimeField(auto_now_add=True)


