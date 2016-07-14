from django.db import models
from challenge.models import Challenge


def upload_to(instance, filename):
    from os import urandom
    return 'avatar/person/' + '.'.join(
        (instance.username, urandom(4).encode('hex'),
        filename.split('.')[-1]))


class Person(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length=20, blank=True)
    motto = models.CharField(max_length=30, blank=True)
    major = models.CharField(max_length=10, default='')
    score = models.PositiveIntegerField(default=0)
    school = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    blog = models.URLField(blank=True)
    avatar = models.ImageField(upload_to=upload_to, default='avatar/person/default.gif')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    group = models.ForeignKey('team.Group', null=True, on_delete=models.SET_NULL, related_name='members')
    challenges = models.ManyToManyField(Challenge, through='Submit', related_name='submitter')
    privilege = models.IntegerField(default=0)
    email_check = models.CharField(max_length=100)
    apply_group = models.ForeignKey('team.Group', null=True, on_delete=models.SET_NULL, related_name='appliers')

    def __unicode__(self):
        return self.username + '_' + self.email


class Submit(models.Model):
    person = models.ForeignKey(Person)
    challenge = models.ForeignKey(Challenge)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField()


class MaxScore(models.Model):
    category = models.CharField(max_length=10)
    score = models.PositiveIntegerField(default=0)
    person = models.ForeignKey(Person, null=True)

    def __unicode__(self):
        return self.category + ': ' + str(self.score)
