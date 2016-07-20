from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from person.models import Person
from news.views import group_contest_news
from datetime import timedelta
import json


def _index(request):
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

OKAY = HttpResponse(
    json.dumps({'msg': 'okay'}),
    content_type='application/json')

FAIL = HttpResponse(
    json.dumps({'msg': 'fail'}),
    content_type='application/json')

ERROR = HttpResponse(
    json.dumps({'msg': 'error'}),
    content_type='application/json')


def index(request):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    groups = Group.objects.order_by('-score')
    if not user.group:
        return render(request, 'group-recruit.jade', {
            'groups': groups,
            'username': username,
        })
    tasks = user.group.tasks.all().order_by('-pk')
    for item in tasks:
        item.assign = item.assign_to.username if item.assign_to else ''
        item.donetime = (item.datetime + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
    return render(request, 'group.jade', {
        'username': username,
        'groupname': user.group.name,
        'avatar': user.group.avatar,
        'code': user.group.code,
        'members': user.group.members.all(),
        'writeups': [],
        'newmembers': [],
        'tasking': filter(lambda x: not x.done, tasks),
        'tasked': filter(lambda x: x.done, tasks)
    })


def join(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        cf = CodeForm(request.POST)
        if cf.is_valid() and not user.group:
            code = cf.cleaned_data['code']
            try:
                group = Group.objects.get(code=code)
                user.group = group
                user.save()
                return HttpResponse(
                    json.dumps({
                        'name': group.name,
                        'msg': 'OKAY'
                    }),
                    content_type='application/json')
            except:
                return FAIL
    return ERROR


def create(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        gf = GroupNameForm(request.POST)
        if gf.is_valid() and not user.group:
            from os import urandom
            name = gf.cleaned_data['name']
            try:
                user.group = Group.objects.create(
                    name=name,
                    leader=user,
                    code=urandom(12).encode('hex')
                )
                user.save()
                return OKAY
            except:
                return FAIL
    return ERROR


def apply(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        gf = GroupForm(request.POST)
        if gf.is_valid() and not user.group:
            pk = gf.cleaned_data['pk']
            user.apply_group = Group.objects.get(pk=pk)
            user.save()
            return OKAY
    return ERROR


def withdraw(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        user.apply_group = None
        user.save()
        return OKAY
    return ERROR


def new_task(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        group = user.group
        tf = TaskForm(request.POST)
        if tf.is_valid():
            try:
                name = tf.cleaned_data['assign']
                assigned_to = Person.objects.get(username=name) if name else None
                deadline = tf.cleaned_data['deadline']
                task = Task.objects.create(
                    group=group,
                    content=tf.cleaned_data['content'],
                )
                if assigned_to:
                    task.assign_to = assigned_to
                if deadline:
                    task.deadline = deadline
                task.save()
                return OKAY
            except:
                return FAIL
    return ERROR


def do_task(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        group = user.group
        tf = GroupForm(request.POST)
        if tf.is_valid():
            try:
                pk = tf.cleaned_data['pk']
                task = Task.objects.get(pk=pk)
                if task.group == group and not task.done:
                    task.done = True
                    task.checker = user
                    task.save()
                    return OKAY
                return FAIL
            except:
                return FAIL
    return ERROR


def clear_task(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        group = user.group
        tf = GroupForm(request.POST)
        if tf.is_valid():
            try:
                pk = tf.cleaned_data['pk']
                task = Task.objects.get(pk=pk)
                if task.group == group:
                    task.delete()
                    return OKAY
                return FAIL
            except:
                return FAIL
    return ERROR