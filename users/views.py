from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
    return render(request, 'users.jade', {
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