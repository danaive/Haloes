# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from team.models import Group, GroupMaxScore
from team.models import recalc_score
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        GroupMaxScore.objects.all().update(score=1)
        for group in Group.objects.all():
            recalc_score(group)
            print '%s: %d\' %d' % (group.name, group.score, group.solved.all().count())
