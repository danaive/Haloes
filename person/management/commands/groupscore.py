# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from person.models import Person
from team.models import Group, GroupMaxScore
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        GroupMaxScore.objects.all().update(score=0)
        for group in Group.objects.all():
            group.solved.clear()
            for user in group.members.all():
                for challenge in user.challenges.filter(submit__status=True):
                    group.solved.add(challenge)
            score = [0, 0, 0, 0, 0]
            cate = {'PWN': 0, 'REVERSE': 1, 'WEB': 2, 'CRYPTO': 3, 'MISC': 4}
            for challenge in group.solved.all():
                group.score += challenge.score
                score[cate[challenge.category]] += challenge.score
            group.save()
            for key in cate:
                gms = GroupMaxScore.objects.get(category=key)
                if score[cate[key]] > gms.score:
                    gms.score = score[cate[key]]
                    gms.save()
            print '%s: %d\'' % (group.name, group.score)
