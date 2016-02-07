from django.shortcuts import render

def index(request):
    return render(request, 'writeup.jade', {
        'writeups': [{
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'misc',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'misc',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'misc',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'misc',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'misc',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'misc',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'misc',
            'author': 'danlei',
            'team': 'DAWN',
            'comment': 15,
            'like': 25
        },
        {
            'title': 'hehehehe',
            'url': 16,
            'challenge': 'dice game',
            'category': 'misc',
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