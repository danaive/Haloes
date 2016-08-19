from django.db import models
from django.contrib.auth.models import User
from contest.models import Contest


class Origin(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.title


class Challenge(models.Model):
    title = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=10,
        choices=(('PWN', 'PWN'), ('REVERSE', 'REVERSE'), ('WEB', 'WEB'), ('CRYPTO', 'CRYPTO'), ('MISC', 'MISC'))
    )
    score = models.PositiveIntegerField()
    flag = models.CharField(max_length=50)
    origin = models.ForeignKey(Origin, null=True)
    status = models.CharField(max_length=3, choices=(('on', 'ON'), ('off', 'OFF')))
    solved = models.PositiveIntegerField(default=0)
    contest = models.ForeignKey(Contest, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    zipfile = models.FileField()
    privilege = models.IntegerField(default=0)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title + str(self.score)


def upload_to(instance, filename):
    from os import urandom
    return 'zipfile/%s.%s' % (filename, urandom(8).encode('hex'))


class Package(models.Model):
    title = models.CharField(max_length=50, unique=True)
    uploader = models.ForeignKey(User)
    zipfile = models.FileField(upload_to=upload_to)
    docker_required = models.BooleanField()
    deployed = models.BooleanField(default=False)
