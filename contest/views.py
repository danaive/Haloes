from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import *
from .forms import *
from person.models import Person
from challenge.models import Challenge
from team.models import Ranking
from news.views import contest_news
from datetime import datetime, timedelta, tzinfo
import json


OKAY = HttpResponse(
    json.dumps({'msg': 'okay'}),
    content_type='application/json')

FAIL = HttpResponse(
    json.dumps({'msg': 'fail'}),
    content_type='application/json')

ERROR = HttpResponse(
    json.dumps({'msg': 'error'}),
    content_type='application/json')


class UTC(tzinfo):
    def __init__(self, offset=8):
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


def challenge(request, pk):
    pk = int(pk)
    challenges = Challenge.objects.filter(contest__pk=pk, public=True)
    team = Person.objects.get(pk=request.session['uid']).team
    solved = Ranking.objects.get(team=team, contest__pk=pk).solved.all()
    for item in challenges:
        item.done = True if item in solved else False
        dic = {'PWN': 'primary', 'REVERSE': 'success', 'WEB': 'danger',
            'CRYPTO': 'info', 'MISC': 'warning'}
        item.cls = dic[item.category]
    return render(request, 'dctf/challenge.jade', {
        'challenges': challenges
    })


def team(request, pk):
    return render(request, 'dctf/team.jade')


def ranking(request, pk):
    return render(request, 'dctf/ranking.jade')


def submit(request):
    if request.is_ajax:
        sf = SubmitForm(request.POST)
        if sf.is_valid():
            pk = sf.cleaned_data['pk']
            flag = sf.cleaned_data['flag']
            contest = sf.cleaned_data['contest']
            try:
                challenge = Challenge.objects.get(pk=pk)
                contest = Contest.objects.get(pk=contest)
            except:
                return ERROR
            user = Person.objects.get(pk=request.session['uid'])
            if flag == challenge.flag:
                Submit.objects.update_or_create(person=user,
                                                challenge=challenge,
                                                defaults={'status': True})
                user.score = user.challenges.filter(
                    submit__status=True
                ).aggregate(Sum('score')['score__sum'])
                user.save()
                maxsc = user.challenges.filter(
                    submit__status=True,
                    category=challenge.category
                ).aggregate(Sum('score'))['score__sum']
                if maxsc > MaxScore.objects.get(
                    category=challenge.category).score:
                    MaxScore.objects.filter(
                        category=challenge.category).update(score=maxsc)
                rank = Ranking.objects.get(team=user.team, contest__pk=contest)
                if challenge not in rank.solved.all():
                    rank.solved.add(challenge)
                return OKAY
            else:
                Submit.objects.update_or_create(
                    person=user,
                    challenge=challenge,
                    defaults={'status': False}
                )
                return FAIL
    return ERROR