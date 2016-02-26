from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Challenge


def index(request):
    # challenges = Challenge.objects.all()
    # return render(request, 'challenge.jade', {
    #         'challenges': challenges
    #     })
    return render(request, 'challenge.jade', {
        'challenges': [{
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': 1,
            'status': 'ton'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': 0,
            'status': 'toff'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': -1,
            'status': 'on'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': -1,
            'status': 'on'
        },
        {
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': 2,
            'status': 'off'
        },],
    })

def classify(request):
    if request.is_ajax:
        cate = request.GET['cate']
        # validation in choice form
        challenges = Challenge.objects.filter(category=cate)
        return json.dumps({'challenges':challenges}, content_type='application/json')

def switch(request): pass