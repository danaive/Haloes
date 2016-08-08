from django.conf import settings
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


def index(request, pk=u'-1'):
    pk = int(pk)
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    groups = Group.objects.order_by('-score')
    if not user.group and pk == -1:
        return render(request, 'group-recruit.jade', {
            'groups': groups,
            'username': username,
        })
    elif pk == -1 or user.group and user.group.pk == pk:
        group = user.group
    else:
        try:
            group = Group.objects.get(pk=pk)
        except:
            return render(request, '404.jade')
    tasks = group.tasks.all().order_by('-pk')
    for item in tasks:
        item.assign = item.assign_to.username if item.assign_to else ''
        item.donetime = (item.datetime + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
    issues = group.issues.all().order_by('-time')
    for item in issues:
        item.name = item.author.username
        item.avatar = item.author.avatar
        item.timex = (item.time + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
        item.comment = item.comments.count()
    return render(request, 'group.jade', {
        'username': username,
        'groupname': group.name,
        'avatar': group.avatar,
        'code': group.code,
        'members': group.members.all(),
        'writeups': [],
        'newmembers': [],
        'tasking': filter(lambda x: not x.done, tasks),
        'tasked': filter(lambda x: x.done, tasks),
        'issues': issues
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


def get_score(request):
    if request.is_ajax:
        gf = GroupNameForm(request.POST)
        if gf.is_valid():
            try:
                group = Group.objects.get(name=gf.cleaned_data['name'])
            except:
                return ERROR
            data = {
                'msg': 'okay',
                'score': [0] * 5,
                'capacity': []
            }
            cate = {'PWN': 0, 'REVERSE': 1, 'WEB': 2, 'CRYPTO': 3, 'MISC': 4}
            for item in group.solved.all():
                data['score'][cate[item.category]] += item.score
            data['capacity'].append({
                'score': map(
                    lambda x: 100 * data['score'][x[1]] / GroupMaxScore.objects.get(category=x[0]).score,
                    sorted(cate.iteritems(), key=lambda x: x[1])
                ),
                'name': group.name
            })
            visitor = Person.objects.get(pk=request.session['uid'])
            if visitor.group and visitor.group != group:
                tmp = [0] * 5
                for item in visitor.group.solved.all():
                    tmp[cate[item.category]] += item.score
                data['capacity'].append({
                    'score': map(
                        lambda x: 100 * tmp[x[1]] / GroupMaxScore.objects.get(category=x[0]).score,
                        sorted(cate.iteritems(), key=lambda x: x[1])
                    ),
                    'name': visitor.group.name
                })
            if sum(data['score']) == 0:
                return FAIL
            return HttpResponse(json.dumps(data), content_type='application/json')
    return ERROR

@csrf_exempt
def update_avatar(request):
    if request.is_ajax:
        iform = ImageForm(request.POST, request.FILES)
        if iform.is_valid():
            img = request.FILES['img']
            if img.size > 5 * 1024 * 1024:
                return HttpResponse(
                    json.dumps({'msg': 'Image No Larger Than 5M is Accepted.'}),
                    content_type='application/json'
                )
            group = Person.objects.get(pk=request.session['uid']).group
            group.avatar = img
            group.save()
            return HttpResponse(json.dumps({
                'msg': 'okay',
                'path': settings.MEDIA_URL + group.avatar,
            }), content_type='application/json')
        return FAIL
    return ERROR


def issue(request, pk=u'-1'):
    user = Person.objects.get(pk=request.session['uid'])
    group = user.group
    pk = int(pk)
    if pk == -1:
        return render(request, 'group-editor.jade', {
            'username': user.username
        })
    try:
        issue = group.issues.get(pk=pk)
        comments = Comment.objects.filter(issue=issue).order_by('-time')
        for item in comments:
            item.avatar = item.author.avatar
            item.writer = item.author.username
            if item.reply:
                item.recver = item.reply.username
            item.pk = item.author.pk
            item.timex = (item.time + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
        return render(request, 'group-issue.jade', {
            'username': user.username,
            'pk': pk,
            'title': issue.title,
            'content': issue.content,
            'author': issue.author.username,
            'authorid': issue.author.pk,
            'avatar': user.avatar,
            'comments': comments
        })
    except:
        return render(request, '404.jade')


def submit(request):
    if request.is_ajax:
        wf = IssueForm(request.POST)
        if wf.is_valid():
            try:
                title = wf.cleaned_data['title']
                content = wf.cleaned_data['content']
                user = Person.objects.get(pk=request.session['uid'])
                wp = Issue.objects.create(
                    author=user,
                    group=user.group,
                    title=title,
                    content=content
                )
                return HttpResponse(json.dumps({
                    'msg': 'okay',
                    'pk': wp.pk
                }), content_type='application/json')
            except:
                return FAIL
    return ERROR


def comment(request):
    if request.is_ajax:
        cf = CommentForm(request.POST)
        if cf.is_valid():
            # try:
            if True:
                comment = Comment.objects.create(
                    author=Person.objects.get(pk=request.session['uid']),
                    issue=Issue.objects.get(pk=cf.cleaned_data['issue']),
                    content=cf.cleaned_data['content']
                )
                reply = cf.cleaned_data['reply']
                if reply:
                    comment.reply = Person.objects.get(pk=reply)
                    comment.save()
                return OKAY
            # except:
            else:
                return FAIL
    return ERROR
