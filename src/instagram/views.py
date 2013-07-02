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

from models import InstaProfile
from src.settings import INS_CLIENT_ID, INS_CLIENT_SECRET, INS_ACCESS_TOKEN_URL, INS_AUTHORIZE_URL, INS_REDIRECT_URL

  #############################
 #####     Instagram     #####
#############################


def insta_main(request):
    return TemplateResponse(request, 'instagram/login.html')


def insta_auth(request):
    # build the url to request
    params = {'client_id': INS_CLIENT_ID,
              'redirect_uri': INS_REDIRECT_URL,
              'response_type': 'code'}
    data = urllib.urlencode(params)
    # redirect the user to the url to confirm access for the app
    return redirect('%s?%s' % (INS_AUTHORIZE_URL, data))


def insta_callback(request):
    # get the code returned from foursquare
    code = request.GET.get('code')

    # build the url to request the access_token
    params = {'client_id': INS_CLIENT_ID,
              'client_secret': INS_CLIENT_SECRET,
              'grant_type': 'authorization_code',
              'redirect_uri': INS_REDIRECT_URL,
              'code': code}
    data = urllib.urlencode(params)
    req = urllib2.Request(INS_ACCESS_TOKEN_URL, data)

    # request the access_token
    response = urllib2.urlopen(req)
    access_token = json.loads(response.read())
    user_id = access_token['user']['id']
    access_token = access_token['access_token']

    # store the access_token & user_id for later use
    request.session['access_token'] = access_token
    request.session['user_id'] = user_id

    # redirect the user to show we're done
    return redirect(reverse('insta_done'))


def insta_done(request):
    # get the access_token
    access_token = request.session.get('access_token')
    user_id = request.session.get('user_id')

    # request user details from foursquare
    params = {'access_token': access_token}
    data = urllib.urlencode(params)
    url = 'https://api.instagram.com/v1/users/%s/' % user_id
    full_url = url + '?' + data
    print full_url
    response = urllib2.urlopen(full_url)
    print response
    response = response.read()
    user_data = json.loads(response)['data']

    try:
        user = User.objects.get(username=user_data['username'])
    except User.DoesNotExist:
        # Save information on user
        user = User(username=user_data['username'],
                    first_name=user_data['full_name'], last_name="",
                    email=user_data['username'] + '@instagram.com')
        user.set_password(access_token)
        user.save()
        profile = InstaProfile()
        profile.user = user
        profile.oauth_token = access_token
        profile.insta_id = user_id
        profile.save()

    user = authenticate(username=user.username, password=user.password)

    login(request, user)

    # show the page with the user's name to show they've logged in
    return redirect(reverse('insta_welcome'))


@login_required
def insta_welcome(request):
    user = request.user
    print user.first_name

    return TemplateResponse(request, 'instagram/welcome.html', {'user': user})


def insta_unauth(request):
    # clear any tokens and logout
    request.session.clear()
    logout(request)
    return redirect(reverse('insta_main'))
