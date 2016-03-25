from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'contest.jade', {
        'contests': [{
            'name': 'WHU CTF 2016',
            'start': '2016-3-3 08:00',
            'length': '36:00',
            'status': 'pending',
            'register': 233,
            'url': 16
        },
        {
            'name': 'WHU CTF',
            'start': '2016-3-3',
            'length': '36:00',
            'status': 'running',
            'register': -1,
            'url': 16
        },
        {
            'name': 'WHU CTF',
            'start': '2016-3-3',
            'length': '36:00',
            'status': 'pending',
            'register': -1,
            'url': 16
        },
        {
            'name': 'WHU CTF',
            'start': '2016-3-3',
            'length': '36:00',
            'status': 'pending',
            'register': -1,
            'url': 16
        },
        {
            'name': 'WHU CTF',
            'start': '2016-3-3',
            'length': '36:00',
            'status': 'ended',
            'register': -1,
            'url': 16
        }, ]
    })
