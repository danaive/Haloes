# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
import json


def _send_email_check(email, username):
    from django.core.mail import send_mail
    from os.path import join
    key = b64encode(urandom(12))
    html = open(join(settings.BASE_DIR, 'email_check.html').read().format(
        username=username,
        domain=settings.DOMAIN_NAME,
        token=key + b64encode(sha256(username + key).digest())
    ))
    send_mail('Email Confirm', 'Email Confirm at Haloes',
        'noreply@' + settings.DOMAIN_NAME, [email], html_message=html)
    return key


@csrf_exempt
def check_email(request, token):
    try:
        key = token[:16]
        user = Person.objects.get(email_check=token)
        if b64encode(sha256(user.name + key).digest()) == token[16:]:
            user.email_check = 'done'
            user.save()
            return HttpResponseRedirect(reverse('person:index'))
    except:
        return ERROR


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
                        username=username,
                        password=password,
                        email=email,
                        nickname=username,
                        email_check=_send_email_check(email, username)
                    )
                    request.session['uid'] = user.pk
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
                from hashlib import sha256
                if sha256(user.password + salt).hexdigest() == password:
                    if user.email_check != 'done':
                        return response('email')
                    request.session['uid'] = user.pk
                    return OKAY
            except:
                return FAIL
    return ERROR


def sign_out(request):
    del request.session['uid']
    return OKAY


@csrf_exempt
def update_avatar(request):
    if request.is_ajax:
        iform = ImageForm(request.POST, request.FILES)
        if iform.is_valid():
            img = request.FILES['img']
            if img.size > 5 * 1024 * 1024:
                return FAIL
            user = Person.objects.get(pk=request.session['uid'])
            user.avatar = img
            user.save()
            return response('okay', {'path': settings.MEDIA_URL + user.avatar})
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
    if pk != -1 and pk != request.session['uid']:
        try:
            owner = Person.objects.get(pk=pk)
            visitor = Person.objects.get(pk=request.session['uid'])
            data['self'] = visitor.username
            if visitor.following.filter(pk=pk):
                data['follow'] = True
        except:
            return render(request, '404.jade')
    else:
        owner = Person.objects.get(pk=request.session['uid'])
    followings = owner.following.all()
    followers = owner.followers.all()
    data.update({
        'username': owner.username,
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
            if sum(data['score']) == 0:
                return FAIL
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
        if user.following.filter(pk=item.pk):
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
        # item.person_set.all().writeup_set.count()
    return render(request, 'ranking.jade', {
        'username': username,
        'apply': False if user.group else True,
        'users': users,
        'groups': groups
    })


def get_news(request):
    if request.is_ajax:
        user = Person.objects.get(pk=request.session['uid'])
        try:
            page = int(request.GET.get('page', 0))
        except:
            return ERROR
        from django.db.models import Q
        if user.group:
            news = News.objects.filter(
                Q(person__in=user.following) | Q(group=user.group)
            ).order_by('-time')[page:page+10]
        else:
            news = News.objects.filter(person__in=user.following)[page:page+10]
        return HttpResponse(json.dumps(news), content_type='application/json')
    return ERROR
