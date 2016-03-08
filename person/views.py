# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
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
    major = forms.CharField(max_length=50)
    school = forms.CharField(max_length=50)
    avatar = forms.URLField()
    email = forms.EmailField()
    blog = forms.URLField()


def register(request):
    if request.is_ajax:
        rform = RegForm(request.POST)
        if rform.is_valid():
            username = rform.cleaned_data['username']
            password = rform.cleaned_data['password']
            email = rform.cleaned_data['email']
            user = Person.objects.filter(username=username)
            if not user:
                Person.objects.create(
                    username = username,
                    password = password,
                    email = email
                )
                request.session['uid'] = username
                return HttpResponse(json.dumps({'msg': 'okay'}), content_type='application/json')
            return HttpResponse(json.dumps({'msg': 'fail'}), content_type='application/json')
    return HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')

def login(request):
    if request.is_ajax:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data['username']
            password = lform.cleaned_data['password']
            salt = lform.cleaned_data['salt']
            user = Person.objects.filter(username=username)
            from hashlib import md5
            if md5(user.password + salt) == password:
                request.session['uid'] = username
                return HttpResponse(json.dumps({'msg': 'okay'}), content_type='application/json')
            return HttpResponse(json.dumps({'msg': 'fail'}), content_type='application/json')
    return HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')

def logout(request): pass


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
            user = Person.objects.get(request.session['uid'])
            user.avatar = img
            return HttpResponse(json.dumps({'msg':'okay'}), content_type='application/json')
    return HttpResponse(json.dumps({'msg':'Invalid Request!'}), content_type='application/json')

def update_info(request):
    # email check to be added
    if request.is_ajax:
        uform = UpdateForm(request.POST)
        if uform.is_valid():
            username = request.session['uname']
            user = Person.objects.get(username=username)
            user.major = uform.cleaned_data['major']
            user.school = uform.cleaned_data['school']
            user.avatar = uform.cleaned_data['avatar']
            user.email = uform.cleaned_data['email']
            user.blog = uform.cleaned_data['blog']
            user.save()
            return HttpResponse(json.dumps({'msg':'okay'}), content_type='application/json')
    return HttpResponse(json.dumps({'msg':'fail'}), content_type='application/json')



#----------------------- DEBUG -----------------------#
def index(request):
    return render(request, 'person.jade', {
        'username': 'danlei',
        'pageuser': 'xiami',
        'major': 'Misc',
        'score': '233',
        'solve': 4,
        'writeup': 2,
        'team': 'DAWN',
        'school': 'WHU',
        'mail': 'jne0915@gmail.com',
        'blog': 'danlei.github.io'
    })

def rank(request):
    return render(request, 'person.jade', {
        'username': 'danlei',
        'pageuser': 'xiami',
        'major': 'Misc',
        'score': '233',
        'solve': 4,
        'writeup': 2,
        'team': 'DAWN',
        'school': 'WHU',
        'mail': 'jne0915@gmail.com',
        'blog': 'danlei.github.io'
    })

@csrf_exempt
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