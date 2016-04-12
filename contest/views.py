from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Contest
from person.models import Person
from news.views import contest_news
from datetime import datetime, timedelta, tzinfo
import json


class UTC(tzinfo):
    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return 'UTC +%s' % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)


def index(request, pk='-1'):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    try:
        contest = Contest.objects.get(pk=int(pk))
        return render(request, 'dctf/challenge.jade')
    except:
        contests = Contest.objects.order_by('-time')
        for item in contests:
            if item.time > timezone.now():
                item.register = item.registered.count()
                item.status = 'pending'
            elif item.time + item.length > timezone.now():
                item.register = -1
                item.status = 'running'
            else:
                item.register = -1
                item.status = 'ended'
            item.start = (item.time +
                timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            item.duration = '%d:00' % (item.length.total_seconds() / 3600)
        return render(request, 'contest.jade', {
            'username': username,
            'contests': contests
        })
