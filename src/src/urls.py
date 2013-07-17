from django.conf.urls import patterns, include, url
from django.views.defaults import *
from src import views


urlpatterns = patterns('',
    url(r'^foursquare/', include('foursquare.urls')),
    url(r'^instagram/', include('instagram.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/complete/$', views.contact_complete, name='contact_complete'),
)
