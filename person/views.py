# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import Person, MaxScore
from team.models import Group
from news.models import News
from news.views import *
from os import urandom
from hashlib import sha256
from base64 import b64encode
from datetime import timedelta
import json


def _send_email_check(email, username, password):
    if settings.DEBUG:
        return 'done'
    from django.core.mail import send_mail
    from os.path import join
    key = urandom(8).encode('hex')
    html = open(join(settings.BASE_DIR, 'email_check.html')).read().format(
        username=username.encode('utf-8'),
        domain=settings.DOMAIN_NAME,
        token=key + sha256(key + password).hexdigest()[:32]
    )
    send_mail('Email Confirm', 'Email Confirm for Haloes',
        'noreply@' + settings.DOMAIN_NAME, [email], html_message=html)
    return key


@csrf_exempt
def check_email(request, token):
    try:
        key = token[:16]
        user = Person.objects.get(email_check=key)
        if sha256(key + user.password).hexdigest()[:32] == token[16:]:
            user.email_check = 'done'
            user.save()
            return HttpResponseRedirect(reverse('login'))
    except:
        return HttpResponse('expired token')


def sign_up(request):
    if request.is_ajax:
        rform = RegForm(request.POST)
        if rform.is_valid():
            username = rform.cleaned_data['username']
            password = rform.cleaned_data['password']
            email = rform.cleaned_data['email']
            if '@' not in username and len(username) <= 16:
                try:
                    assert Person.objects.filter(username=username) or Person.objects.filter(email=email)
                    user = Person.objects.create(
                        username=username,
                        password=password,
                        email=email,
                        nickname=username,
                        email_check=_send_email_check(email, username, password)
                    )
                    return OKAY
                except:
                    pass
            return FAIL
    return ERROR


def sign_in(request):
    if request.is_ajax:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data['username']
            password = lform.cleaned_data['password']
            salt = lform.cleaned_data['salt']
            try:
                if '@' not in username:
                    user = Person.objects.get(username=username)
                else:
                    user = Person.objects.get(email=username)
                if sha256(user.password + salt).hexdigest() == password:
                    if user.email_check != 'done':
                        return response('email')
                    try:
                        Session.objects.get(pk=user.session_key).delete()
                    except:
                        pass
                    user.session_key = request.session.session_key
                    user.save()
                    request.session['uid'] = user.pk
                    request.session[user.email] = '233'
                    return OKAY
            except:
                return FAIL
    return ERROR


def sign_out(request):
    try:
        user = Person.objects.get(pk=request.session['uid'])
        user.session_key = ''
    except:
        pass
    request.session.flush()
    request.session.cycle()
    return OKAY


@csrf_exempt
def update_avatar(request):
    if request.is_ajax:
        iform = ImageForm(request.POST, request.FILES)
        if iform.is_valid():
            img = request.FILES['img']
            if img.size > 500 * 1024:
                return FAIL
            user = Person.objects.get(pk=request.session['uid'])
            user.avatar = img
            user.save()
            from PIL import Image
            img = Image.open(user.avatar.path)
            img.resize((120, 120), Image.ANTIALIAS).save(user.avatar.path, 'PNG')
            return response('okay', {'path': user.avatar.url})
        return FAIL
    return ERROR


def update_info(request):
    if request.is_ajax:
        uform = UpdateForm(request.POST)
        if uform.is_valid():
            user = Person.objects.get(pk=request.session['uid'])
            email = uform.cleaned_data['email']
            if email and email != user.email:
                user.check_email = _send_email_check(email)
            for attr in ['major', 'school', 'email', 'blog', 'motto']:
                if uform.cleaned_data[attr]:
                    setattr(user, attr, uform.cleaned_data[attr])
            user.save()
            data = {
                'major': user.major,
                'school': user.school,
                'email': user.email,
                'blog': user.blog,
                'motto': user.motto,
            }
            return response('okay', data)
    return ERROR


def login(request):
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
                return ERROR
            follower = Person.objects.get(pk=request.session['uid'])
            if follower.following.filter(pk=user.pk):
                follower.following.remove(user)
            else:
                follower.following.add(user)
            return OKAY
    return ERROR


def index(request, pk=u'-1'):
    pk = int(pk)
    data = {}
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
        try:
            owner = Person.objects.get(pk=pk)
        except:
            owner = user
        if owner == user:
            data['self'] = True
        elif owner in user.following.all():
            data['follow'] = True
        data['username'] = user.username
    else:
        user = None
        try:
            owner = Person.objects.get(pk=pk)
        except:
            return HttpResponseRedirect(reverse('ranking'))
        data['username'] = None
    followings = owner.following.all()
    followers = owner.followers.all()
    data.update({
        'ownername': owner.username,
        'motto': owner.motto,
        'major': owner.major,
        'score': owner.score,
        'solve': owner.challenges.filter(submit__status=True).count(),
        'writeup': owner.writeup_set.count(),
        'group': owner.group.name if owner.group else '',
        'school': owner.school,
        'email': owner.email,
        'blog': owner.blog,
        'avatar': owner.avatar,
        'followings': followings,
        'followers': followers,
        'followingNum': len(followings),
        'followersNum': len(followers),
    })
    return render(request, 'person.jade', data)


def score(request):
    if request.is_ajax:
        sform = FollowForm(request.POST)
        if sform.is_valid():
            try:
                user = Person.objects.get(username=sform.cleaned_data['username'])
            except:
                return ERROR
            data = {
                'score': [0] * 5,
                'capacity': []
            }
            cate = {'PWN': 0, 'REVERSE': 1, 'WEB': 2, 'CRYPTO': 3, 'MISC': 4}
            for challenge in user.challenges.filter(submit__status=True):
                data['score'][cate[challenge.category]] += challenge.score
            data['capacity'].append({
                'score': map(
                    lambda x: 100 * data['score'][x[1]] / MaxScore.objects.get(category=x[0]).score,
                    sorted(cate.iteritems(), key=lambda x: x[1])
                ),
                'name': user.username
            })
            try:
                visitor = Person.objects.get(pk=request.session['uid'])
                if visitor.username != user.username:
                    tmp = [0] * 5
                    for challenge in visitor.challenges.filter(
                        submit__status=True):
                        tmp[cate[challenge.category]] += challenge.score
                    data['capacity'].append({
                        'score': map(
                            lambda x: 100 * tmp[x[1]] / MaxScore.objects.get(category=x[0]).score,
                            sorted(cate.iteritems(), key=lambda x: x[1])
                        ),
                        'name': visitor.username
                    })
            except:
                pass
            # if sum(data['score']) == 0:
            #     return FAIL
            return response('okay', data)
    return ERROR


def ranking(request):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    users = Person.objects.order_by('-score')
    for item in users:
        item.writeup = item.writeup_set.count()
        item.solved = item.challenges.filter(submit__status=True).count()
        item.fstate = 0
        if user and user.following.filter(pk=item.pk):
            item.fstate = 1
            if item.following.filter(pk=user.pk):
                item.fstate = 2
    groups = Group.objects.order_by('-score')
    for item in groups:
        item.membern = item.members.count()
        item.solvedn = item.solved.count()
        item.writeup = reduce(
            lambda x, y: x + y,
            map(lambda x: x.writeup_set.count(), item.members.all())
        )
    return render(request, 'ranking.jade', {
        'username': username,
        'apply': False if user and user.group else True,
        'users': users,
        'groups': groups
    })


def get_news(request, pk=u'-1'):
    if request.is_ajax:
        pk = int(pk)
        step = 6
        try:
            page = int(request.POST.get('page', 0))
            user = Person.objects.get(pk=request.session['uid'])
            focus = Person.objects.get(pk=pk) if pk != -1 and pk != user.pk else None
        except:
            return ERROR
        from django.db.models import Q
        if focus:
            news = News.objects.filter(person=focus).order_by('-time')[page:page+step]
        elif user.group:
            news = News.objects.filter(
                Q(person__in=user.following.all(), public=True) | Q(group=user.group) | Q(person=user)
            ).order_by('-time')[page:page+step]
        else:
            news = News.objects.filter(
                Q(person__in=user.following.all(), public=True) | Q(person=user)
            ).order_by('-time')[page:page+step]
        if news:
            newsx = []
            for item in news.values():
                itemx = {}
                itemx['time'] = (item['time'] + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
                itemx['title'] = item['title']
                itemx['content'] = item['content']
                itemx['link'] = item['link']
                itemx['avatar'] = item['avatar']
                newsx.append(itemx)
            return response('okay', {'news': newsx})
        return FAIL
    return ERROR
