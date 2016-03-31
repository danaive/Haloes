from django.db import models


class News(models.Model):
    title = models.CharField(max_length=30)
    avatar = models.ImageField()
    link = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)
