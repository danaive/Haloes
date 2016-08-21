from .models import *
from django.http import HttpResponse
import json


'''The views of News doesn't accept HTTP request,
but offer methods to save News and wrapped constants of HTTP response.
'''


def response(msg, data=None):
    dic = {'msg': msg}
    if data:
        dic.update(data)
    return HttpResponse(json.dumps(dic), content_type='application/json')


OKAY = response('okay')
FAIL = response('fail')
ERROR = response('error')


def submit_news(user, challenge, writeup):
    News.objects.create(
        title=user.username,
        avatar=user.avatar,
        link='/person/%d/' % user.pk,
        content="submitted writeup <a href='/writeup/{pk}/'>{writeup}</a> of {title}({cate} {score}').".format(
            writeup=writeup.title,
            title=challenge.title,
            cate=challenge.category,
            score=challenge.score,
            pk=writeup.pk
        ),
        person=user,
        group=user.group
    )


def solve_news(user, challenge):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='/person/%d/' % user.pk,
        content="solved challenge <a href='/challenge/{pk}/'>{title}</a>({cate} {score}\').".format(
            title=challenge.title,
            cate=challenge.category,
            score=challenge.score,
            pk=challenge.pk
        ),
        person=user,
        group=user.group
    )


def group_contest_news(group, contest):
    News.objects.create(
        title=group.name, avatar=group.avatar,
        link='/group/%d/' % group.pk,
        content="registered for the contest <a href='/contest/{pk}/'>{contest}</a>, start at {time}.".format(
            contest=contest.title,
            time=contest.time,
            pk=contest.pk
        ),
        person=group.leader,
        group=group
    )


def contest_news(user, contest):
    News.objects.create(
        title=user.username,
        avatar=user.avatar,
        link='/person/%d/' % user.pk,
        content="added a practice contest <a href='/contest/{pk}/'>{contest}</a>, start at {time}.".format(
            contest=contest.title,
            time=contest.time,
            pk=contest.pk
        ),
        person=user,
        group=user.group
    )
