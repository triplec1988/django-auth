Author
=======
Chris Clouten

django-auth
===========

Using OAuth to create and authenticate new users is wonderful, but it can be a pain to set everything up and make sure users are both being created, authenticated, and logged in from their third party application credentials. Django-Auth is an alternative to larger libraries django-social and meant to be an easy to understand example application for how to implement OAuth into your own applications for authentication and user creation. The steps I followed are listed below:

Step 1
=======

Register your application with the appropriate third party application. In this case I used Foursquare and Instagram as examples. It can really be anything that supports OAuth. Once you register your application, create variables in your settings.py file for the client_id and client_secret you will be privided. Additionally, create your redirect_uri and set that as a variable in settings along with the authentication and access_token URLs the third party application provides you.

Step 2
=======

Set up your urls.py file. In each application I have a set of URLs that begins with a basic login page and runs through callback, authentication, creation ('done') and welcome. I also include URLs for logout.

Step 3
=======

Set up your views.py file to support your URLs. This file will need to import the variables you have stored in settings.py. This is also a great time to create your templates. This application only uses two: login.html and welcome.html. The views are also going to be where you create and save a user to the auth_user table of Django, as well as any additional information you'd like to store from the response JSON. I have set up models.py to extend the core Django User model to store some additional information.

Step 4
=======

This is the real meat of it. When trying to create, save, and authenticate users through OAuth you need to create a custom backend. This is essentially a custom authenticate() method to authorize the new users you created. Examples of this are in backends.py in each app. You can authenticate based on whatever variables you wish, in this case I simple am authenticating based on username and password. After you create backends.py you need to add this to your AUTHENTICATION_BACKENDS in settings.py, as I have done. This will tell Django to check these backends in addition to the default (ModelBackend) when authenticating users through OAuth.

Step 5
=======

Test it out. After following these steps you should now be able to create users and save them to the database.

Usage
======

This example is free to use for anyone. All I ask is that if you do use some of the code or examples you try to give me credit.

Contribute
===========

If you wish to create additional apps within this project to create examples for other third party applications other than Foursquare and Instagram just fork this repo, add the app and submit a pull request. I'll be happy to add you as a contributor.
