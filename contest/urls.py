from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/challenge/$', views.challenge),
    url(r'^(?P<pk>\d+)/ranking/$', views.ranking),
    url(r'^(?P<pk>\d+)/team/$', views.team),
    url(r'^submit/$', views.submit),
]
