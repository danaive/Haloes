# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django import forms
from .models import Person
import json


class RegForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    salt = forms.CharField(max_length=50)

class ImageForm(forms.Form):
    image = forms.ImageField()

class UpdateForm(forms.Form):
    major = forms.CharField(max_length=50, required=False)
    school = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    blog = forms.URLField(required=False)


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
                    return HttpResponse(json.dumps({'msg': 'fail'}), content_type='application/json')
                else:
                    request.session['uid'] = user.pk
                    return HttpResponse(json.dumps({'msg': 'okay'}), content_type='application/json')
            return HttpResponse(json.dumps({'msg': 'fail'}), content_type='application/json')
    return HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')

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
                return HttpResponse(json.dumps({'msg': 'okay'}), content_type='application/json')
            return HttpResponse(json.dumps({'msg': 'fail'}), content_type='application/json')
    return HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')

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
            return HttpResponse(json.dumps({'msg':'okay'}), content_type='application/json')
    return HttpResponse(json.dumps({'msg':'Invalid Request!'}), content_type='application/json')

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
    return HttpResponse(json.dumps({'msg':'error'}), content_type='application/json')

def login(request):
    from os import urandom
    salt = urandom(8).encode('hex')
    request.session['salt'] = salt
    return render(request, 'login.jade', {
        'wtfs': [i for i in range(66)],
        'salt': salt
    })

def index(request, pageowner=''):
    if pageowner:
        try:
            user = Person.objects.get(username=pageowner)
        except:
            return render(request, 'person.jade')
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
    if pageowner:
        data['self'] = Person.objects.get(pk=request.session['uid']).username
    return render(request, 'person.jade', data)



######################## DEBUG ########################
def rank(request):
    return render(request, 'signin.jade', {
        'wtfs': [i for i in range(66)]
    })


def score(request):
    return HttpResponse(json.dumps({
        'score': [123,65,83,25,233],
        'capacity': [
            {
                'name': 'danlei',
                'score': [65, 59, 90, 81, 56]
            },
            {
                'name': 'xiami',
                'score': [28, 48, 40, 19, 96]
            }
        ]
    }), content_type='application/json')


def writeup(request):
    return render(request, 'writeup.jade', {})