# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import Person, MaxScore
from team.models import Team
import json

OKAY = HttpResponse(json.dumps({'msg': 'okay'}), content_type='application/json')
FAIL = HttpResponse(json.dumps({'msg': 'fail'}), content_type='application/json')
ERROR = HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')

def sign_up(request):
    if request.is_ajax:
        rform = RegForm(request.POST)
        if rform.is_valid():
            username = rform.cleaned_data['username']
            password = rform.cleaned_data['password']
            email = rform.cleaned_data['email']
            msg = 'fail'
            if '@' not in username and len(username) <= 16:
                try:
                    user = Person.objects.create(
                        username = username,
                        password = password,
                        email = email,
                        nickname = username
                    )
                except:
                    return FAIL
                else:
                    request.session['uid'] = user.pk
                    return OKAY
            return FAIL
    return ERROR

def sign_in(request):
    if request.is_ajax:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data['username']
            password = lform.cleaned_data['password']
            salt = lform.cleaned_data['salt']
            if '@' not in username:
                user = Person.objects.filter(username=username)
            else:
                user = Person.objects.filter(email=username)
            from hashlib import sha256
            if user and sha256(user[0].password + salt).hexdigest() == password:
                request.session['uid'] = user[0].pk
                return OKAY
            return FAIL
    return ERROR

def sign_out(request):
    del request.session['uid']
    return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def update_avatar(request):
    if request.is_ajax:
        iform = ImageForm(request.POST, request.FILES)
        if iform.is_valid():
            img = request.FILES['img']
            if img.size > 5 * 1024 * 1024:
                return HttpResponse(json.dumps({'msg':'Image No Larger Than 5M is Accepted.'}), content_type='application/json')
            print img.content_type
            user = Person.objects.get(pk=request.session['uid'])
            user.avatar = img
            user.save()
            return HttpResponse(json.dumps({
                'msg': 'okay',
                'path': settings.MEDIA_URL + user.avatar.name,
            }), content_type='application/json')
        return FAIL
    return ERROR

def update_info(request):
    # email check to be added
    if request.is_ajax:
        uform = UpdateForm(request.POST)
        if uform.is_valid():
            user = Person.objects.get(pk=request.session['uid'])
            attrs = ['major', 'school', 'email', 'blog', 'motto']
            for attr in attrs:
                if uform.cleaned_data[attr]:
                    setattr(user, attr, uform.cleaned_data[attr])
            user.save()
            return HttpResponse(json.dumps({
                'msg': 'okay',
                'major': user.major,
                'school': user.school,
                'email': user.email,
                'blog': user.blog,
                'motto': user.motto,
            }), content_type='application/json')
    return ERROR

def login(request):
    from os import urandom
    salt = urandom(8).encode('hex')
    request.session['salt'] = salt
    return render(request, 'login.jade', {
        'wtfs': [i for i in range(66)],
        'salt': salt
    })

def follow(request):
    if request.is_ajax:
        fform = FollowForm(request.POST)
        if fform.is_valid():
            try:
                user = Person.objects.get(username=fform.cleaned_data['username'])
            except:
                return render(request, '404.jade')
            else:
                follower = Person.objects.get(pk=request.session['uid'])
                follower.follow.add(user)
                return OKAY
    return ERROR

def index(request, page_user=''):
    if page_user:
        try:
            user = Person.objects.get(username=page_user)
        except:
            return render(request, '404.jade')
    else:
        user = Person.objects.get(pk=request.session['uid'])
    data = {
        'username': user.username,
        'motto': user.motto,
        'major': user.major,
        'score': user.score,
        'solve': user.challenges.filter(submit__status=True).count(),
        'writeup': user.writeup_set.count(),
        'team': user.team.name if user.team else '',
        'school': user.school,
        'email': user.email,
        'blog': user.blog,
        'avatar': user.avatar,
    }
    if page_user:
        visitor = Person.objects.get(pk=request.session['uid'])
        data['self'] = visitor.username
        if visitor.follow.filter(username=page_user):
            data['follow'] = True
    return render(request, 'person.jade', data)

def score(request):
    if request.is_ajax:
        sform = FollowForm(request.POST)
        if sform.is_valid():
            try:
                user = Person.objects.get(username=sform.cleaned_data['username'])
            except:
                return render(request, '404.jade')
            else:
                data = {
                    'score': [0] * 5,
                    'capacity': []
                }
                cate = {'PWN': 0, 'REVERSE': 1, 'WEB': 2, 'CRYPTO': 3, 'MISC': 4}
                for challenge in user.challenges.filter(submit__status=True):
                    data['score'][cate[challenge.category]] += challenge.score
                data['capacity'].append({
                    'score': map(
                        lambda ct: 100 * data['score'][ct[1]] / max(MaxScore.objects.get(category=ct[0]).score, 1),
                        cate.iteritems()),
                    'name': user.username
                })
                visitor = Person.objects.get(pk=request.session['uid'])
                if visitor.username != user.username:
                    tmp = [0] * 5
                    for challenge in visitor.challenges.filter(submit__status=True):
                        tmp[cate[challenge.category]] += challenge.score
                    data['capacity'].append({
                        'score': map(
                            lambda ct: 100 * tmp[ct[1]] / MaxScore.objects.get(category=ct[0]),
                            cate.iteritems()),
                        'name': visitor.username
                    })
                if sum(data['score']) == 0:
                    data['score'][0] = 1
                return HttpResponse(json.dumps(data), content_type='application/json')
        return ERROR

def ranking(request):
    user = Person.objects.get(pk=request.session['uid'])
    users = Person.objects.order_by('-score')
    for item in users:
        item.writeup = item.writeup_set.count()
        item.solved = item.challenges.filter(submit__status=True).count()
        item.fstate = 0
        if item in user.follow.all():
            item.fstate = 1
            if user in item.follow.all():
                item.fstate = 2
    teams = Team.objects.order_by('-score')
    for item in teams:
        item.members = item.person_set.count()
        item.writeup = item.person_set.writeup_set.count()
    return render(request, 'ranking.jade', {
        'apply': False if user.team else True,
        'users': users,
        'teams': teams
    })
