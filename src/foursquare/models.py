from django.db import models
from django.contrib.auth.models import User


class FoursqProfile(models.Model):
    user = models.ForeignKey(User)
    oauth_token = models.CharField(max_length=200)
