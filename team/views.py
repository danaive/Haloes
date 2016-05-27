from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from person.models import Person
from news.views import group_contest_news
import json


def index(request):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    return render(request, 'group.jade', {
        'username': username,
        'newmember': 1,
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
