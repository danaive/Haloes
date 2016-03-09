from django.db import models
from challenge.models import Challenge

def upload_to(instance, filename):
    return 'avatar/person/' + instance.username + filename.split('.')[-1]

class Person(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    major = models.CharField(max_length=10, default='')
    score = models.PositiveIntegerField(default=0)
    school = models.CharField(max_length=50, blank=True)
    mail = models.EmailField()
    blog = models.URLField()
    avatar = models.ImageField(upload_to=upload_to)
    follow = models.ManyToManyField('self', symmetrical=False)
    team = models.ForeignKey('team.Team', null=True, blank=True, on_delete=models.SET_NULL)
    submits = models.ManyToManyField(Challenge, through='Submit')


class Submit(models.Model):
    person = models.ForeignKey(Person)
    challenge = models.ForeignKey(Challenge)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
