from django.shortcuts import render
from person.models import Person
from news.views import submit_news


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


def detail(request, pk): pass


def submit(request): pass


def comment(request, pk): pass


def like(request, pk): pass


def unlike(request, pk): pass


def star(request, pk): pass


def unstar(request, pk): pass


def test(request):
    return render(request, 'editor.jade')