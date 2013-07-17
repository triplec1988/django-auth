from django.conf.urls import patterns, url

from instagram import views

urlpatterns = patterns('',
    # Instagram Authentication
    url(r'^callback/$', views.insta_callback, name='insta_callback'),
    url(r'^logout/$', views.insta_unauth, name='insta_unauth'),
    url(r'^auth/$', views.insta_auth, name='insta_auth'),
    url(r'^done/$', views.insta_done, name='insta_done'),
    url(r'^welcome/$', views.insta_welcome, name='insta_welcome'),
)
