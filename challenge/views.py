from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Challenge
from .forms import *
from person.models import Person


def index(request):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    challenges = Challenge.objects.all()
    attrs = ['url', 'title', 'source', 'score', 'solved', 'status']
    cha_list = []
    for challenge in challenges:
        cha_item = {}
        for attr in attrs:
            cha_item[attr] = getattr(challenge, attr)
        cha_list.append(cha_item)
    if user:
        # state:
        #  -1: not tried
        #   0: attampted
        #   1: solved
        #   2: team-solved
        for i, challenge in enumerate(challenges):
            state = -1
            if challenge in user.submits.filter(submit__status=False):
                state = 0
            elif challenge in user.submits.filter(submit__status=True):
                state = 1
            elif user.team and challenge in user.team.solved.all():
                state = 2
            cha_list[i]['state'] = state
    return render(request, 'challenge.jade', {
        'username': username,
        'challenges': cha_list
    })

def switch(request): pass