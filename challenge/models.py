from django.db import models
from contest.models import Contest


def upload_to(instance, filename):
    from os import urandom
    return 'challenge/source/' + '.'.join(
        (instance.title, urandom(4).encode('hex'),
        'zip'))


class Challenge(models.Model):
    title = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=10)
    score = models.PositiveIntegerField()
    flag = models.CharField(max_length=50)
    source = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=10)
    solved = models.PositiveIntegerField(default=0)
    contest = models.ForeignKey(Contest, null=True, blank=True,
                                on_delete=models.SET_NULL)
    url = models.URLField(blank=True)
    description = models.TextField()
    zipfile = models.FileField()
    privilege = models.IntegerField(default=0)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title + str(self.score)
