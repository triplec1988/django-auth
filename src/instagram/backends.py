from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class InstagramBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            print "Looks like this user does not exist"
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
