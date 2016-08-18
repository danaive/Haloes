from django.contrib import admin
from .models import *


class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'group', 'privilege')


class MaxScoreAdmin(admin.ModelAdmin):
    list_display = ('category', 'score')


admin.site.register(Person, PersonAdmin)
admin.site.register(MaxScore, MaxScoreAdmin)
