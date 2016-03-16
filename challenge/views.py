# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import json
from .models import Challenge
from person.models import Person, Submit

OKAY = HttpResponse(json.dumps({'msg': 'okay'}), content_type='application/json')
FAIL = HttpResponse(json.dumps({'msg': 'fail'}), content_type='application/json')
ERROR = HttpResponse(json.dumps({'msg': 'error'}), content_type='application/json')

def index(request):
    if request.session.get('uid', None):
        user = Person.objects.get(pk=request.session['uid'])
    else:
        user = None
    username = user.username if user else None
    challenges = Challenge.objects.all()
    attrs = ['pk', 'title', 'source', 'score', 'solved', 'status']
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
            if challenge in user.challenges.filter(submit__status=False):
                state = 0
            elif challenge in user.challenges.filter(submit__status=True):
                state = 1
            elif user.team and challenge in user.team.solved.all():
                state = 2
            cha_list[i]['state'] = state
    return render(request, 'challenge.jade', {
        'username': username,
        'challenges': [{
            'pk': 15,
            'title': 'xorlist',
            'source': '0ctf_2016',
            'category': 'MISC',
            'score': 4,
            'solved': 0,
            'status': 'toff',
            'state': 0,
        }] * 32
    })

def switch(request):
    import time
    time.sleep(2)
    return OKAY

class DropForm(forms.Form):
    pk = forms.IntegerField()


class SubmitForm(forms.Form):
    pk = forms.IntegerField()
    flag = forms.CharField()


def drop_attempt(request):
    if request.is_ajax:
        cf = DropForm(request.POST)
        if cf.is_valid():
            pk = cf.cleaned_data['pk']
            try:
                challenge = Challenge.objects.get(pk=pk)
            except:
                return FAIL
            else:
                user = Person.objects.get(pk=request.session['uid'])
                Submit.objects.filter(person=user, challenge=challenge).delete()
                return OKAY
    return ERROR

def submit(request):
    if request.is_ajax:
        cf = SubmitForm(request.POST)
        if cf.is_valid():
            pk = cf.cleaned_data['pk']
            flag = cf.cleaned_data['flag']
            try:
                challenge = Challenge.objects.get(pk=pk)
            except:
                return ERROR
            else:
                user = Person.objects.get(pk=request.session['uid'])
                if flag == challenge.flag:
                    Submit.objects.update_or_create(
                        person = user,
                        challenge = challenge,
                        defaults = {'status': True}
                    )
                    return OKAY
                else:
                    Submit.objects.update_or_create(
                        person = user,
                        challenge = challenge,
                        defaults = {'status': False}
                    )
                    return FAIL
    return ERROR
