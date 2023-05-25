from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    todo_token = models.CharField(max_length=200, null=True, blank=True)
    cf_handle = models.CharField(max_length=200, null=True, blank=True)
    at_handle = models.CharField(max_length=200, null=True, blank=True)
    lc_handle = models.CharField(max_length=200, null=True, blank=True)
    tp_handle = models.CharField(max_length=200, null=True, blank=True)
