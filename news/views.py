# -*- coding: utf-8 -*-
from .models import *
from django.http import HttpResponse
from datetime import timedelta
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


def submit_news(writeup):
    News.objects.update_or_create(
        title=writeup.author.username,
        avatar=writeup.author.avatar.url,
        link='/person/%d/' % writeup.author.pk,
        content="submitted writeup <a href='/writeup/{pk}/'>{writeup}</a> of {title}({cate} {score}').".format(
            writeup=writeup.title.encode('utf-8'),
            title=writeup.challenge.title.encode('utf-8'),
            cate=writeup.challenge.category,
            score=writeup.challenge.score,
            pk=writeup.pk
        ),
        person=writeup.author,
        group=writeup.author.group
    )


def solve_news(user, challenge):
    News.objects.create(
        title=user.username,
        avatar=user.avatar.url,
        link='/person/%d/' % user.pk,
        content="solved challenge <a href='/challenge/{pk}/'>{title}</a>({cate} {score}\').".format(
            title=challenge.title.encode('utf-8'),
            cate=challenge.category,
            score=challenge.score,
            pk=challenge.pk
        ),
        person=user,
        group=user.group
    )


def join_group(user, group):
    News.objects.update_or_create(
        title=user.username,
        avatar=user.avatar.url,
        link='/person/%d/' % user.pk,
        content="joined group <a href='/group/{pk}/'>{group}</a>.".format(
            group=group.name.encode('utf-8'),
            pk=group.pk
        ),
        person=user,
        group=group
    )


def group_task(user, group, assigned):
    News.objects.create(
        title=group.name,
        avatar=group.avatar.url,
        link='/group/',
        content='{leader} assigned new task to you.'.format(
            leader=user.username.encode('utf-8')
        ),
        person=assigned,
        public=False
    )


def group_issue(user, group):
    news.objects.create(
        title=group.name,
        avatar=group.avatar.url,
        link='/group/',
        content='new issue was published by {author}.'.format(
            author=user.username.encode('utf-8')
        ),
        group=group
    )


def apply_group(user, group):
    News.objects.update_or_create(
        title=user.username,
        avatar=user.avatar.url,
        link='/person/%d/' % user.pk,
        content="submitted application for the membership of {group}.".format(
            group=group.name.encode('utf-8')
        ),
        group=group
    )


def group_contest(group, contest):
    News.objects.create(
        title=group.name,
        avatar=group.avatar.url,
        link='/group/%d/' % group.pk,
        content="registered for the contest <a href='/contest/{pk}/'>{contest}</a>, start at {time}.".format(
            contest=contest.title.encode('utf-8'),
            time=(contest.time + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'),
            pk=contest.pk
        ),
        person=group.leader,
        group=group
    )


def contest_news(user, contest):
    News.objects.create(
        title=user.username,
        avatar=user.avatar.url,
        link='/person/%d/' % user.pk,
        content="added a practice contest <a href='/contest/{pk}/'>{contest}</a>, start at {time}.".format(
            contest=contest.title.encode('utf-8'),
            time=(contest.time + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M'),
            pk=contest.pk
        ),
        person=user,
        group=user.group
    )
