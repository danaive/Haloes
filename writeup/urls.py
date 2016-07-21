from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^editor/$', views.editor),
    url(r'^(?P<pk>\d+)/editor/$', views.editor),
    url(r'^comment/$', views.comment),
    url(r'^(?P<pk>\d+)/like/$', views.like),
    url(r'^(?P<pk>\d+)/star/$', views.star),
    url(r'^upload-image/$', views.upload_image),
    url(r'^get-challenges/$', views.get_challenges),
    url(r'^submit/$', views.submit),
]
