# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
from person.models import *
from team.models import *
from writeup.models import *
from contest.models import *
from news.views import *
import json
import zipfile
import re


def index(request):
    if request.session.get('uid', None):
        user = Person.objects.get(session_key=request.session.session_key)
    else:
        user = None
    username = user.username if user else None
    challenges = Challenge.objects.all()
    attrs = ['pk', 'title', 'origin', 'score', 'status', 'privilege']
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
            elif user.group and user.group.solved.filter(pk=challenge.pk):
                state = 2
            cha_list[i]['state'] = state
            cha_list[i]['category'] = str(challenge.category)
            cha_list[i]['solved'] = challenge.submit_set.filter(
                status=True).count()
    return render(request, 'challenge.jade', {
        'username': username,
        'challenges': cha_list,
        'privilege': user.privilege if user else -1
    })


def drop_attempt(request):
    if request.is_ajax:
        cf = ChallengeForm(request.POST)
        if cf.is_valid():
            pk = cf.cleaned_data['pk']
            try:
                challenge = Challenge.objects.get(pk=pk)
            except:
                return FAIL
            user = Person.objects.get(session_key=request.session.session_key)
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
                user = Person.objects.get(session_key=request.session.session_key)
            except:
                return ERROR
            if flag == challenge.flag:
                state, _ = Submit.objects.update_or_create(
                    person=user,
                    challenge=challenge,
                    defaults={'status': True}
                )
                solved = user.challenges.filter(submit__status=True)
                if state:
                    challenge.solved += 1
                    challenge.save()
                    solve_news(user, challenge)
                else:
                    return OKAY
                user.score = solved.aggregate(Sum('score'))['score__sum']
                user.save()
                maxsc = solved.filter(
                    category=challenge.category
                ).aggregate(Sum('score'))['score__sum']
                ms = MaxScore.objects.get(category=challenge.category)
                if maxsc > ms.score:
                    ms.score = maxsc
                    ms.save()
                if user.group:
                    group = user.group
                    group.solved.add(challenge)
                    group.score = group.solved.all().aggregate(
                        Sum('score'))['score__sum']
                    score = group.solved.filter(
                        category=challenge.category
                    ).aggregate(Sum('score'))['score__sum']
                    gms = GroupMaxScore.objects.get(category=challenge.category)
                    if score > gms.score:
                        gms.score = score
                        gms.save()
                    group.save()
                return OKAY
            else:
                Submit.objects.update_or_create(
                    person=user,
                    challenge=challenge,
                    defaults={'status': False}
                )
                return FAIL
    return ERROR


def detail(request):
    if request.is_ajax:
        cf = ChallengeForm(request.POST)
        if cf.is_valid():
            pk = cf.cleaned_data['pk']
            try:
                challenge = Challenge.objects.get(pk=pk)
            except:
                return ERROR
            return response('okay', {'content': challenge.description})
    return ERROR


def switch(request):
    """Switch Challenge State
    Docker is used to employ challenges. We use Docker Python API
    to turn on or off a particular challenge. the Container
    name is {challenge.pk}_{challenge.name}.

    Args:
        request: Ajax-POST HTTPRequest, contains pk and state field
            pk: the primary key of challenge
            state: the state to be switched

    Returns:
        HTTPResponce: application/json data, two constants are used
            OKAY: the challenge is switched successfully
            ERROR: some error occured
    """
    if request.is_ajax:
        sf = SwitchForm(request.POST)
        if sf.is_valid():
            try:
                challenge = Challenge.objects.get(pk=sf.cleaned_data['pk'])
                user = Person.objects.get(session_key=request.session.session_key)
                if user.privilege > challenge.privilege:
                    return FAIL
            except:
                return ERROR
            # true is on, false is off
            state = sf.cleaned_data['state']
            from docker import Client
            url = "tcp://{ip}:{port}".format(
                ip=settings.DOCKER_IP,
                port=settings.DOCKER_PORT
            )
            version = settings.DOCKER_VERSION
            cotainer_name = "{pk}_{name}".format(
                pk=challenge.pk,
                name=challenge.title
            )
            client = Client(base_url=url, version=version)
            try:
                if state:
                    client.start(container_name)
                else:
                    client.stop(container_name)
            except:
                return ERROR
            return OKAY
    return ERROR


def search(request, pk=u'-1'):
    if request.session.get('uid', None):
        user = Person.objects.get(session_key=request.session.session_key)
    else:
        user = None
    username = user.username if user else None
    ret = {'username': username, 'ucnt': 0, 'privilege': user.privilege}
    if int(pk) != -1:
        ret['challenges'] = Challenge.objects.filter(pk=int(pk))
        ret['xpersons'] = []
        ret['writeups'] = []
        ret['groups'] = []
        ret['contests'] = []
        ret['ucnt'] = -1
        if not ret['challenges']:
            return HttpResponseRedirect(reverse('challenge:index'))
        return render(request, 'search.jade', ret)
    value = request.GET.get('q', None)
    if value == '':
        return render(request, 'search.jade', ret)
    from django.db.models import Q
    ret['xpersons'] = Person.objects.filter(
        Q(username__icontains=value) | Q(school__icontains=value)
    )
    ret['challenges'] = Challenge.objects.filter(
        Q(title__icontains=value) | Q(origin__title__icontains=value)
    )
    ret['writeups'] = Writeup.objects.filter(
        Q(title__icontains=value) | Q(author__username__icontains=value)
    )
    ret['groups'] = Group.objects.filter(name__icontains=value)
    ret['contents'] = Contest.objects.filter(title__icontains=value)
    ret['ucnt'] = sum(map(lambda x: 0 if x[0][0] in 'up' else x[1].count(),
                          ret.iteritems()))
    if ret['groups']:
        for item in ret['groups']:
            item.member = item.members.count()
            item.solvedn = item.solved.count()
            item.writeup = Writeup.objects.filter(
                author__in=item.members.all()).count()
        if user:
            ret['apply'] = -1 if not user or not user.apply_group else user.apply_group.pk
    return render(request, 'search.jade', ret)
