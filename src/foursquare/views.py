from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import urllib
import urllib2
import json

from models import FoursqProfile
from src.settings import FSQ_CLIENT_ID, FSQ_CLIENT_SECRET, FSQ_ACCESS_TOKEN_URL, FSQ_AUTHORIZE_URL, FSQ_REDIRECT_URL


  ##############################
 #####     FOURSQUARE     #####
##############################


def foursq_auth(request):
    # build the url to request
    params = {'client_id': FSQ_CLIENT_ID,
              'response_type': 'code',
              'redirect_uri': FSQ_REDIRECT_URL}
    data = urllib.urlencode(params)
    # redirect the user to the url to confirm access for the app
    return redirect('%s?%s' % (FSQ_AUTHORIZE_URL, data))


def foursq_callback(request):
    # get the code returned from foursquare
    code = request.GET.get('code')

    # build the url to request the access_token
    params = {'client_id': FSQ_CLIENT_ID,
              'client_secret': FSQ_CLIENT_SECRET,
              'grant_type': 'authorization_code',
              'redirect_uri': FSQ_REDIRECT_URL,
              'code': code}
    data = urllib.urlencode(params)
    req = urllib2.Request(FSQ_ACCESS_TOKEN_URL, data)

    # request the access_token
    response = urllib2.urlopen(req)
    access_token = json.loads(response.read())
    access_token = access_token['access_token']

    # store the access_token for later use
    request.session['access_token'] = access_token

    # redirect the user to show we're done
    return redirect(reverse('foursq_done'))


def foursq_done(request):
    # get the access_token
    access_token = request.session.get('access_token')

    # request user details from foursquare
    params = {'oauth_token': access_token}
    data = urllib.urlencode(params)
    url = 'https://api.foursquare.com/v2/users/self'
    full_url = url + '?' + data
    response = urllib2.urlopen(full_url)
    response = response.read()
    user_data = json.loads(response)['response']['user']

    try:
        user = User.objects.get(username=user_data['contact']['email'])
    except User.DoesNotExist:
        # Save information on user
        user = User(username=user_data['contact']['email'],
                    first_name=user_data['firstName'], last_name=user_data['lastName'],
                    email=user_data['contact']['email'])
        user.set_password(access_token)
        user.save()
        profile = FoursqProfile()
        profile.user = user
        profile.oauth_token = access_token
        profile.save()

    user = authenticate(username=user.username, password=user.password)

    login(request, user)

    # show the page with the user's name to show they've logged in
    return redirect(reverse('foursq_welcome'))


@login_required
def foursq_welcome(request):
    user = request.user
    print user.first_name

    return TemplateResponse(request, 'foursquare/welcome.html', {'user': user})


def foursq_unauth(request):
    # clear any tokens and logout
    request.session.clear()
    logout(request)
    return redirect(reverse('index'))
