from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check-in/(?P<token>\w+)/$', views.check_email, name='check_in'),
    url(r'^sign-up/$', views.sign_up, name='sign_up'),
    url(r'^sign-in/$', views.sign_in, name='sign_in'),
    url(r'^sign-out/$', views.sign_out, name='sign_out'),
    url(r'^update-avatar/$', views.update_avatar, name='update_avatar'),
    url(r'^update-info/$', views.update_info, name='update_info'),
    url(r'^get-score/$', views.score, name='score'),
    url(r'^follow/$', views.follow, name='follow'),
    url(r'^(?P<pk>\d+)/$', views.index, name='index'),
]
