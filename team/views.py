from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json


def index(request):
    return render(request, 'team.jade', {
        'newmember': 1,
        'rankings': [{
            'name': 'BCTF 2015',
            'rank': 3,
            'total': 700,
            'url': 16
        }],
        'writeups': [{
            'url': 15,
            'title': 'DAWN',
            'time': '2015-12-12',
            'challenge': 'dice game',
            'comment': 15,
            'like': 25,
            'author': 'danlei'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'time': '2015-12-12',
            'challenge': 'dice game',
            'comment': 15,
            'like': 25,
            'author': 'danlei'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'time': '2015-12-12',
            'challenge': 'dice game',
            'comment': 15,
            'like': 25,
            'author': 'danlei'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'time': '2015-12-12',
            'challenge': 'dice game',
            'comment': 15,
            'like': 25,
            'author': 'danlei'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'time': '2015-12-12',
            'challenge': 'dice game',
            'comment': 15,
            'like': 25,
            'author': 'danlei'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'time': '2015-12-12',
            'challenge': 'dice game',
            'comment': 15,
            'like': 25,
            'author': 'danlei'
        }],
        'members': [{
            'name': 'danlei',
            'avatar': '/static/img/danlei.jpg',
            'url': '1',
            'major': 'MISC',
            'score': 233,
            'univ': 'WHU',
        },
        {
            'name': 'danlei',
            'avatar': '/static/img/danlei.jpg',
            'url': '#',
            'major': 'MISC',
            'score': 233,
            'univ': 'WHU',
        },
        {
            'name': 'danlei',
            'avatar': '/static/img/danlei.jpg',
            'url': '#',
            'major': 'MISC',
            'score': 233,
            'univ': 'WHU',
        },
        {
            'name': 'danlei',
            'avatar': '/static/img/danlei.jpg',
            'url': '#',
            'major': 'MISC',
            'score': 233,
            'univ': 'WHU',
        }],
        'newmembers': [{
            'name': 'danlei',
            'avatar': '/static/img/danlei.jpg',
            'url': '#',
            'major': 'MISC',
            'score': 233,
            'univ': 'WHU',
        },
        {
            'name': 'danlei',
            'avatar': '/static/img/danlei.jpg',
            'url': '#',
            'major': 'MISC',
            'score': 233,
            'univ': 'WHU',
        },
        {
            'name': 'danlei',
            'avatar': '/static/img/danlei.jpg',
            'url': '#',
            'major': 'MISC',
            'score': 233,
            'univ': 'WHU',
        },
        {
            'name': 'danlei',
            'avatar': '/static/img/danlei.jpg',
            'url': '#',
            'major': 'MISC',
            'score': 233,
            'univ': 'WHU',
        }],
    })


def _team_contest_news(team, contest):
    News.objects.create(
        title=team.name, avatar=team.avatar,
        link='#team-' + team.pk,
        content='registered for the contest {contest}, \
                 start at {time}.'.format(
                     contest=contest.title,
                     time=contest.time),
        person=team.leader, team=team
    )