from django.shortcuts import render
from person.models import Person

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


def _submit_news(user, challenge, writeup):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + user.pk,
        content='submitted writeup {writeup} \
                 of {title}({cate} {score}).'.format(
                     writeup=writeup.title, title=challenge.title,
                     cate=challenge.category, score=challenge.score),
        person=user, team=user.team
    )
