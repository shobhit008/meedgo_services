from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from decimal import *
from users.models import CustomeUser


class pharmacistDetails(models.Model):
    user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE, null=True, blank=True)
    licence_image = models.FileField(default='default.jpg', upload_to='pharmacit_pics', null=True, blank=True)
    registration_image = models.FileField(default='default.jpg', upload_to='pharmacit_pics', null=True, blank=True)
    id_image = models.FileField(default='default.jpg', upload_to='pharmacit_pics', null=True, blank=True)
    tan_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.user.mobile_number    