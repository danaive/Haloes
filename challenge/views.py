from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return render(request, 'challenge.jade', {
        'challenges': [{
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': 1,

        },
        {
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': 0
        },
        {
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': -1
        },
        {
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': -1
        },
        {
            'url': 15,
            'title': 'DAWN',
            'source': '31c3_2015',
            'score': 300,
            'solved': 3,
            'state': 2
        },],
        'st': -1
    })