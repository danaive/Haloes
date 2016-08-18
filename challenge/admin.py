from django.contrib import admin
from .models import *


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'origin', 'score', 'status', 'privilege')
    fieldsets = [
        (None, {'fields': ['title', 'status', 'privilege']}),
        (None, {'fields': ['category', 'contest', 'origin', 'flag', 'solved']}),
        (None, {'fields': ['zipfile', 'description', 'score', 'public']})
    ]


class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'docker_required', 'deployed')

    def deploy_challenge(self, request, queryset):
        pass



admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Package, PackageAdmin)