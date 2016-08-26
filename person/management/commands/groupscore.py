# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from person.models import Person
from team.models import Group
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        for group in Group.objects.all():
            group.solved.clear()
            for user in group.members.all():
                for challenge in user.challenges.filter(submit__status=True):
                    group.solved.add(challenge)
            for challenge in group.solved.all():
                group.score += challenge.score
            group.save()
            print '%s: %d\'' % (group.name, group.score)
