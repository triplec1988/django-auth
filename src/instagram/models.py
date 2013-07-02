from django.db import models
from django.contrib.auth.models import User


class InstaProfile(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.CharField(max_length=200)
    insta_id = models.CharField(max_length=32)
