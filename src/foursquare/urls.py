from django.conf.urls import patterns, url

from foursquare import views

urlpatterns = patterns('',
    # Foursquare Authentication
    url(r'^callback/$', views.foursq_callback, name='foursq_callback'),
    url(r'^logout/$', views.foursq_unauth, name='foursq_unauth'),
    url(r'^auth/$', views.foursq_auth, name='foursq_auth'),
    url(r'^done/$', views.foursq_done, name='foursq_done'),
    url(r'^welcome/$', views.foursq_welcome, name='foursq_welcome'),
)
