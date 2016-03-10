# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from .forms import *
from .models import Person, MaxScore
import json

okay = HttpResponse(json.dumps({'msg': 'okay'}), content_type='application/json')
fail = HttpResponse(json.dumps({'msg': 'fail'}), content_type='application/json')
error = HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')
e404 = render(request, '404.jade')

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
                        email = email
                    )
                except:
                    return fail
                else:
                    request.session['uid'] = user.pk
                    return okay
            return fail
    return error

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
                return okay
            return fail
    return error

def sign_out(request):
    del request.session['uid']
    return HttpResponseRedirect(reverse('login'))

def update_avatar(request):
    if request.is_ajax:
        iform = ImageForm(request.POST, request.FILES)
        if iform.is_valid():
            img = iform.FILES['img']
            if img.size > 5 * 1024 * 1024:
                return HttpResponse(json.dumps({'msg':'Image No Larger Than 5M is Accepted.'}), content_type='application/json')
            from os import path, popen
            filepath = path.join(settings.MEDIA_ROOT, 'tmp', request.session['uid'])
            with open(filepath, 'wb+') as fw:
                for chunk in img.chunks:
                    fw.write(chunk)
            suffix = popen('file ' + filepath).read().split(':')[-1].strip().split()[0]
            if suffix not in ['GIF', 'JPEG', 'PNG'] or suffix != filepath.split('.')[-1].upper():
                return HttpResponse(json.dumps({'msg':'Invalid File Type!'}), content_type='application/json')
            user = Person.objects.get(pk=request.session['uid'])
            user.avatar = img
            return okay
    return error

def update_info(request):
    # email check to be added
    if request.is_ajax:
        uform = UpdateForm(request.POST)
        if uform.is_valid():
            user = Person.objects.get(pk=request.session['uid'])
            attr = ['major', 'school', 'email', 'blog']
            map(lambda x: setattr(user, x, uform.cleaned_data[x]) if uform.cleaned_data[x] else None, attr)
            user.save()
            return HttpResponse(json.dumps({
                'msg':'okay',
                'major': user.major,
                'school': user.school,
                'email': user.email,
                'blog': user.blog
            }), content_type='application/json')
    return error

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
                return e404
            else:
                follower = Person.objects.get(pk=request.session['uid'])
                follower.follow.add(user)
                return okay
    return error

def index(request, page_user=''):
    if page_user:
        try:
            user = Person.objects.get(username=page_user)
        except:
            return e404
    else:
        user = Person.objects.get(pk=request.session['uid'])
    data = {
        'username': user.username,
        'major': user.major,
        'score': user.score,
        'solve': user.submits.filter(status=True).count(),
        'writeup': user.writeup_set.count(),
        'team': user.team.name if user.team else '',
        'school': user.school,
        'email': user.email,
        'blog': user.blog,
    }
    if page_user:
        visitor = Person.objects.get(pk=request.session['uid'])
        data['self'] = visitor.username
        if visitor.follow.filter(username=page_user):
            data['follow'] = True
    return render(request, 'person.jade', data)

def _score(request):
    if request.is_ajax:
        sform = FollowForm(request.POST)
        if sform.is_valid():
            try:
                user = Person.objects.get(username=sform.cleaned_data['username'])
            except:
                return e404
            else:
                data = {
                    'score': [0] * 5,
                    'capacity': []
                }
                cate = {'PWN': 0, 'REVERSE': 1, 'WEB': 2, 'CRYPTO': 3, 'MISC': 4}
                for submit in user.submits.filter(status=True)):
                    data['score'][cate[submit.challenge.category]] += submit.challenge.score
                data['capacity'].append({
                    'score': map(
                        lambda ct: 100 * data['score'][ct[1]] / MaxScore.objects.get(category=ct[0]),
                        cate.iteritems()),
                    'name': user.username
                })
                visitor = Person.objects.get(pk=request.session['uid'])
                if visitor.username != user.username:
                    tmp = [0] * 5
                    for submit in visitor.submits.filter(status=True)):
                        tmp[cate[submit.challenge.category]] += submit.challenge.score
                    data['capacity'].append({
                        'score': map(
                            lambda ct: 100 * tmp[ct[1]] / MaxScore.objects.get(category=ct[0]),
                            cate.iteritems()),
                        'name': visitor.username
                    })
                if sum(data['score']) == 0:
                    data['score'][0] = 1
                return HttpResponse(json.dumps(data), content_type='application/json')
        return error



######################## DEBUG ########################
def rank(request):
    return render(request, 'signin.jade', {
        'wtfs': [i for i in range(66)]
    })


def score(request):
    return HttpResponse(json.dumps({
        'score': [123,65,83,25,233],
        # 'score': [0,0,0,0,0],
        'capacity': [
            # {
            #     'name': 'danlei',
            #     # 'score': [65, 59, 90, 81, 56]
            #     'score': [0,0,0,0,0],
            # },
            {
                'name': 'xiami',
                'score': [28, 48, 40, 19, 96]
            }
        ]
    }), content_type='application/json')


def writeup(request):
    return render(request, 'writeup.jade', {})