# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from person.models import Person
from writeup.models import Writeup
from news.views import *
from datetime import timedelta
import json


def index(request, pk=u'-1'):
    pk = int(pk)
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    if (not user or not user.group) and pk == -1:
        groups = Group.objects.order_by('-score')
        for item in groups:
            item.member = item.members.count()
            item.solvedn = item.solved.count()
            item.writeup = Writeup.objects.filter(author__in=item.members.all()).count()
        return render(request, 'group-recruit.jade', {
            'groups': groups,
            'username': username,
            'apply': -1 if not user or not user.apply_group else user.apply_group.pk
        })
    elif user and (pk == -1 or user.group.pk == pk):
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
    writeups = Writeup.objects.filter(author__in=group.members.all())
    cate = {'PWN': 'primary', 'REVERSE': 'success', 'WEB': 'danger', 'CRYPTO': 'info', 'MISC': 'warning'}
    for item in writeups:
        item.like = item.likes.count()
        item.comment = item.comments.count()
        item.avatar = item.author.avatar
        item.cate = cate[item.challenge.category]
    solved = group.solved.all()
    ret = {
        'username': username,
        'groupname': group.name,
        'avatar': group.avatar,
        'code': group.code,
        'members': group.members.all(),
        'newmembers': group.appliers.all(),
        'newmember': group.appliers.count(),
        'writeups': writeups,
        'tasking': filter(lambda x: not x.done, tasks),
        'tasked': filter(lambda x: x.done, tasks),
        'issues': issues,
        'state': 0 if user not in group.members.all() else 1 if user == group.leader else 2
    }
    for item in cate:
        tmp = solved.filter(category=item)
        ret.update({
            '%sList' % item: tmp,
            '%sNum' % item: tmp.count()
        })
    return render(request, 'group.jade', ret)

def join(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        cf = CodeForm(request.POST)
        if cf.is_valid() and not user.group:
            code = cf.cleaned_data['code']
            try:
                group = Group.objects.get(code=code)
                group.solved.add(user.challenges.filter(submit__status=True))
                user.group = group
                user.save()
                join_group(user, group)
                return response('okay', {'name': group.name})
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
        gf = IntForm(request.POST)
        if gf.is_valid() and not user.group:
            pk = gf.cleaned_data['pk']
            group = Group.objects.get(pk=pk)
            user.apply_group = group
            user.save()
            apply_group(user, group)
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
                assigned_to = Person.objects.get(username=name) if name != 'Unassigned' else None
                deadline = tf.cleaned_data['deadline']
                task = Task.objects.create(
                    group=group,
                    content=tf.cleaned_data['content'],
                )
                if assigned_to:
                    task.assign_to = assigned_to
                    group_task(user, group, assigned_to)
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
        tf = IntForm(request.POST)
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
        tf = IntForm(request.POST)
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
            # if sum(data['score']) == 0:
            #     return FAIL
            return response('okay', data)
    return ERROR


@csrf_exempt
def update_avatar(request):
    if request.is_ajax:
        iform = ImageForm(request.POST, request.FILES)
        if iform.is_valid():
            img = request.FILES['img']
            if img.size > 500 * 1024:
                return FAIL
            group = Person.objects.get(pk=request.session['uid']).group
            group.avatar = img
            group.save()
            from PIL import Image
            img = Image.open(group.avatar.path)
            img.resize((120, 120), Image.ANTIALIAS).save(group.avatar.path, 'PNG')
            return response('okay', {'path': group.avatar.url})
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
                group_issue(user, user.group)
                return response('okay', {'pk': wp.pk})
            except:
                return FAIL
    return ERROR


def comment(request):
    if request.is_ajax:
        cf = CommentForm(request.POST)
        if cf.is_valid():
            try:
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
            except:
                return FAIL
    return ERROR


def approve(request):
    if request.is_ajax:
        gf = IntForm(request.POST)
        if gf.is_valid():
            try:
                user = Person.objects.get(pk=request.session['uid'])
                approved = Person.objects.get(pk=gf.cleaned_data['pk'])
                group = user.group
                if not approved.group and user == group.leader:
                    group.members.add(approved)
                    for item in user.challenges.filter(submit__status=True):
                        group.solved.add(item)
                    approved.apply_group = None
                    approved.save()
                    join_group(approved, group)
                    return OKAY
            except:
                pass
        return FAIL
    return ERROR


def kickout(request):
    if request.is_ajax:
        gf = IntForm(request.POST)
        if gf.is_valid():
            try:
                user = Person.objects.get(pk=request.session['uid'])
                kicked = Person.objects.get(pk=gf.cleaned_data['pk'])
                group = user.group
                if kicked.group == group and user == group.leader:
                    group.members.remove(kicked)
                    return OKAY
            except:
                pass
        return FAIL
    return ERROR


def dismiss(request):
    user = Person.objects.get(pk=request.session['uid'])
    if user.group and user.group.leader == user:
        user.group.delete()
        user.group = None
        return HttpResponseRedirect(reverse('team:index'))
    else:
        return render(request, '403.jade')
