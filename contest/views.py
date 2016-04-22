from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import Sum
from .models import *
from .forms import *
from person.models import Person
from challenge.models import Challenge
from team.models import *
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
        return render(request, 'dctf/overview.jade', {
            'contest': contest.title,
            'username': username,
            'introduce': None
        })
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
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    pk = int(pk)
    try:
        challenges = Challenge.objects.filter(contest__pk=pk, public=True)
        team = Person.objects.get(pk=request.session['uid']).team
        solved = map(
            lambda x: x.challenge,
            Ranking.objects.get(team=team, contest__pk=pk).solved.all()
        )
    except:
        return render(request, '404.jade')
    for item in challenges:
        item.done = True if item in solved else False
        dic = {'PWN': 'primary', 'REVERSE': 'success', 'WEB': 'danger',
            'CRYPTO': 'info', 'MISC': 'warning'}
        item.cls = dic[item.category]
    return render(request, 'dctf/challenge.jade', {
        'username': username,
        'challenges': challenges,
        'contest': Contest.objects.get(pk=pk).title
    })


def team(request, pk):
    pk = int(pk)
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    team = user.team
    contest = Contest.objects.get(pk=pk)
    rank = Ranking.objects.get(team=team, contest=contest)
    submits = rank.solved.all()
    for item in submits:
        item.time = item.date
        item.title = item.challenge.title
        item.score = item.challenge.score
        item.cate = item.challenge.category
        item.solver = item.person.username
    return render(request, 'dctf/team.jade', {
        'avatar': team.avatar,
        'teamname': team.name,
        'score': rank.score,
        'ranking': 123,  #### update here
        'username': username,
        'contest': contest.title,
        'challenges': submits
    })


def ranking(request, pk):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    users = Person.objects.filter(team__ranks__pk=pk).order_by('-score')
    for index, item in enumerate(users):
        item.index = index + 1
        challenge = item.challenges.filter(submit__status=True,
                                           contest__pk=pk)
        item.solved = challenge.count()
        item.score = challenge.aggregate(Sum('score'))['score__sum']
        item.fstate = 0
        if user.following.filter(pk=item.pk):
            item.fstate = 1
            if item.following.filter(pk=user.pk):
                item.fstate = 2
    teams = Team.objects.filter(ranks__pk=pk).order_by('-score')
    for index, item in enumerate(teams):
        item.index = index + 1
        item.members = item.person_set.count()
        item.solvedn = Ranking.objects.get(
            team=item, contest__pk=pk).solved.count()
        # item.person_set.all().writeup_set.count()
    return render(request, 'dctf/ranking.jade', {
        'username': username,
        'apply': False if user.team else True,
        'users': users,
        'teams': teams,
        'contest': Contest.objects.get(pk=pk).title
    })


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
                _, submit = Submit.objects.update_or_create(person=user,
                    challenge=challenge, defaults={'status': True})
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
                    rank.solved.add(submit)
                    rank.score += challenge.score
                    rank.save()
                return OKAY
            else:
                Submit.objects.update_or_create(
                    person=user,
                    challenge=challenge,
                    defaults={'status': False}
                )
                return FAIL
    return ERROR