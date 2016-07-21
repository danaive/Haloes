from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^join/$', views.join, name='join'),
    url(r'^create/$', views.create, name='create'),
    url(r'^apply/$', views.apply, name='apply'),
    url(r'^withdraw/$', views.withdraw, name='withdraw'),
    url(r'^new-task/$', views.new_task),
    url(r'^do-task/$', views.do_task),
    url(r'^clear-task/$', views.clear_task),
]
