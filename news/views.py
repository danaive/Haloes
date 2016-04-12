def motto_news(user):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + user.pk,
        content='updated motto: ' + user.motto,
        person=user, team=user.team
    )


def submit_news(user, challenge, writeup):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + user.pk,
        content='submitted writeup {writeup} \
                 of {title}({cate} {score}).'.format(
                     writeup=writeup.title, title=challenge.title,
                     cate=challenge.category, score=challenge.score),
        person=user, team=user.team
    )


def solve_news(user, challenge):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + user.pk,
        content='solved challenge {title} of {cate} {score}.'.format(
            title=challenge.title, cate=challenge.category,
            score=challenge.score),
        person=user, team=user.team
    )


def team_contest_news(team, contest):
    News.objects.create(
        title=team.name, avatar=team.avatar,
        link='#team-' + team.pk,
        content='registered for the contest {contest}, \
                 start at {time}.'.format(
                     contest=contest.title,
                     time=contest.time),
        person=team.leader, team=team
    )


def contest_news(user, contest):
    News.objects.create(
        title=user.username, avatar=user.avatar,
        link='#user-' + user.pk,
        content='added a practice contest {contest}, \
                 start at {time}.'.format(
                     contest=contest.title,
                     time=contest.time),
        person=user, team=user.team
    )
