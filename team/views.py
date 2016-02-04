from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'team.jade', {
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