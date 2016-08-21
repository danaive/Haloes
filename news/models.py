from django.db import models
from person.models import Person
from team.models import Group


class News(models.Model):
    title = models.CharField(max_length=30)
    avatar = models.ImageField()
    link = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)
    person = models.ForeignKey(Person, null=True)
    group = models.ForeignKey(Group, null=True)
    public = models.BooleanField(default=True)