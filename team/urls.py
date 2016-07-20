from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^join/$', views.join, name='join'),
    url(r'^create/$', views.create, name='create'),
    url(r'^apply/$', views.apply, name='apply'),
    url(r'^withdraw/$', views.withdraw, name='withdraw'),
    url(r'^newTask/$', views.new_task),
]
