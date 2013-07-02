from django.conf.urls import patterns, include, url
from django.views.defaults import *


urlpatterns = patterns('',
    url(r'^foursquare/', include('foursquare.urls')),
    url(r'^instagram/', include('instagram.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)
