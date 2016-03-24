# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import Challenge
from person.models import *
import json, zipfile, re

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
    attrs = ['pk', 'title', 'source', 'score', 'solved', 'status', 'privilege']
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
            elif user.team and user.team.solved.filter(pk=challenge.pk):
                state = 2
            cha_list[i]['state'] = state
    return render(request, 'challenge.jade', {
        'username': username,
        'challenges': cha_list,
        'privilege': user.privilege
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
            user = Person.objects.get(pk=request.session['uid'])
            if flag == challenge.flag:
                Submit.objects.update_or_create(
                    person = user,
                    challenge = challenge,
                    defaults = {'status': True}
                )
                maxsc = user.challenges.filter(submit__status=True, category=challenge.category)
                if maxsc > MaxScore.objects.get(category=challenge.category).score:
                    MaxScore.objects.filter(category=challenge.category).update(score=maxsc)
                return OKAY
            else:
                Submit.objects.update_or_create(
                    person = user,
                    challenge = challenge,
                    defaults = {'status': False}
                )
                return FAIL
    return ERROR

def get_challenge(request):
    if request.is_ajax:
        cf = ChallengeForm(request.POST)
        if cf.is_valid():
            pk = cf.cleaned_data['pk']
            try:
                challenge = Challenge.objects.get(pk=pk)
            except:
                return ERROR
            return HttpResponse(json.dumps({
                'msg': 'okay',
                'content': challenge.description
            }), content_type='application/json')


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
                user = Person.objects.get(pk=request.session['uid'])
                if user.privilege > challenge.privilege:
                    return FAIL
            except:
                return ERROR
            # true is on, false is off
            state = sf.cleaned_data['state']
            from docker import Client
            url = "tcp://{ip}:{port}".format(ip=settings.DOCKER_IP, port=settings.DOCKER_PORT)
            version = settings.DOCKER_VERSION
            cotainer_name = "{pk}_{name}".format(pk=challenge.pk, name=challenge.title)
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

@csrf_exempt
def upload(request):
    if request.is_ajax:
        zf = ZipForm(request.POST, request.FILES)
        if zf.is_valid():
            from os import urandom
            zipname = urandom(8).encode('hex')
            filepath = settings.MEDIA_ROOT + 'source/' + zipname + '.zip'
            with open(filepath, 'wb+') as fw:
                for chunk in request.FILES['source']:
                    fw.write(chunk)
            try:
                zip = zipfile.ZipFile(filepath)
                config = json.loads(zip.read('config.json'))
                title = config['title']
                dlpath = config['category'] + '/' + config['title']
                para = {}
                for item in config['statics']:
                    zip.extract(item, settings.MEDIA_ROOT + dlpath)
                    para[item] = settings.MEDIA_URL + dlpath + '/' + item
                if config['dockerfile']:
                    # docker deployment begin

                    para['port'] = 'some port'

                    # end

                pat = re.compile(r'#{\s*(\S+)\s*}')
                opt = {}
                if 'source' in config:
                    opt['source'] = config['source']
                if 'contest' in config:
                    opt['contest'] = config['contest']
                if 'privilege' in config:
                    opt['privilege'] = config['privilege']
                Challenge.objects.update_or_create(
                    title = config['title'],
                    category = config['category'],
                    score = config['score'],
                    flag = config['flag'],
                    zipfile = filepath,
                    description = pat.sub(r'%(\1)s', config['content']) % para,
                    status = 'off' if config['dockerfile'] else 'on',
                    defaults = opt
                )
                return OKAY
            except:
                return ERROR
