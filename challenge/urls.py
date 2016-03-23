from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^drop-attempt/$', views.drop_attempt, name='drop-attempt'),
    url(r'^switch/$', views.switch, name='switch'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^upload/$', views.upload, name='upload'),
]
