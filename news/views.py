from .models import *


def motto_news(user):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + str(user.pk),
        content='updated motto: ' + user.motto,
        person=user, group=user.group
    )


def submit_news(user, challenge, writeup):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + user.pk,
        content='submitted writeup {writeup} \
                 of {title}({cate} {score}).'.format(
                     writeup=writeup.title, title=challenge.title,
                     cate=challenge.category, score=challenge.score),
        person=user, group=user.group
    )


def solve_news(user, challenge):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + user.pk,
        content='solved challenge {title} of {cate} {score}.'.format(
            title=challenge.title, cate=challenge.category,
            score=challenge.score),
        person=user, group=user.group
    )


def group_contest_news(group, contest):
    News.objects.create(
        title=group.name, avatar=group.avatar,
        link='#group-' + group.pk,
        content='registered for the contest {contest}, \
                 start at {time}.'.format(
                     contest=contest.title,
                     time=contest.time),
        person=group.leader, group=group
    )


def contest_news(user, contest):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + user.pk,
        content='added a practice contest {contest}, \
                 start at {time}.'.format(
                     contest=contest.title,
                     time=contest.time),
        person=user, group=user.group
    )
