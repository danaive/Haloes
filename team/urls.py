from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.index),
    url(r'^join/$', views.join, name='join'),
    url(r'^create/$', views.create, name='create'),
    url(r'^apply/$', views.apply, name='apply'),
    url(r'^withdraw/$', views.withdraw, name='withdraw'),
    url(r'^new-task/$', views.new_task),
    url(r'^do-task/$', views.do_task),
    url(r'^clear-task/$', views.clear_task),
    url(r'^get-score/$', views.get_score),
    url(r'^update-avatar/$', views.update_avatar),
    url(r'^issue/$', views.issue),
    url(r'^issue/(?P<pk>\d+)/$', views.issue),
    url(r'^submit/$', views.submit),
    url(r'^comment/$', views.comment),
]
