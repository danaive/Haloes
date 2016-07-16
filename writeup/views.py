from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from person.models import Person
from challenge.models import *
from news.views import submit_news
from .forms import *
import json


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
    return render(request, 'writeup.jade', {
        'username': username,
        'writeups': [{
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'MISC',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'MISC',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'MISC',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'MISC',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'MISC',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'MISC',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'MISC',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'MISC',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        }],
        'mywu': [{
            'url': 15,
            'title': 'DAWN',
            'time': '2015-12-12',
            'challenge': 'dice game',
            'comment': 15,
            'like': 25
        },
        {
            'url': 15,
            'title': 'DAWN',
            'time': '2015-12-12',
            'challenge': 'dice game',
            'comment': 15,
            'like': 25
        }],
        'starredwu': [{
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
        'minelen': 14,
        'starredlen': 20
    })


def edit(request, pk=u'-1'):
    pk = int(pk)
    if pk == -1:
        return OKAY
    else:
        return OKAY


def comment(request, pk): pass


def like(request, pk): pass


def unlike(request, pk): pass


def star(request, pk): pass


def unstar(request, pk): pass


def editor(request):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    sources = map(lambda x: x.title, Source.objects.all())

    return render(request, 'writeup-editor.jade', {
        'username': username,
        'sources': sources,
    })


@csrf_exempt
def upload_image(request):
    if request.is_ajax:
        iform = ImageForm(request.POST, request.FILES)
        if iform.is_valid():
            img = request.FILES['img']
            if img.size > 5 * 1024 * 1024:
                return HttpResponse(
                    json.dumps(
                        {'msg': 'Image No Larger Than 5M is Accepted.'}),
                    content_type='application/json'
                )
            from os import urandom
            from base64 import b64encode
            filename = b64encode(urandom(12)).replace('/', '=')
            filepath = settings.MEDIA_ROOT + 'image/' + filename
            with open(filepath, 'wb+') as dest:
                for chunk in img.chunks():
                    dest.write(chunk)
            return HttpResponse(json.dumps({
                'msg': 'okay',
                'path': settings.MEDIA_URL + 'image/' + filename
            }), content_type='application/json')
        return FAIL
    return ERROR


def get_challenges(request):
    if request.is_ajax:
        sf = SourceForm(request.POST)
        if sf.is_valid():
            title = sf.cleaned_data['title']
            challenges = map(lambda x: {'pk': x.pk, 'name': x.title},
                             Challenge.objects.filter(source=title))
            return HttpResponse(json.dumps({
                'msg': 'okay',
                'challenges': challenges
            }),content_type='application/json')
        return FAIL
    return ERROR


def submit(request):
    if request.is_ajax:
        wf = WriteupForm(request.POST)
        if wf.is_valid():
            try:
                title = wf.cleaned_data['title']
                challenge = Challenge.objects.get(pk=wf.cleaned_data['challenge'])
                content = wf.cleaned_data['content']
                print title
                print challenge
                print content
                print Person.objects.get(pk=request.session['uid'])
                wp = Writeup.objects.create(
                    author=Person.objects.get(pk=request.session['uid']),
                    title=title,
                    challenge=challenge,
                    content=content
                )
                print '456'
                return HttpResponse(json.dumps({
                    'msg': 'okay',
                    'pk': wp.pk
                }), content_type='application/json')
            except:
                return FAIL
    return ERROR


def detail(request, pk):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    try:
        wp = Writeup.objects.get(pk=int(pk))
        return render(request, 'writeup-detail.jade', {
            'username': username,
            'content': wp.content,

        })
    except:
        return render(request, '404.jade')
