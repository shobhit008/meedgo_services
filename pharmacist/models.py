from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from decimal import *
from users.models import CustomeUser, Medicine, Order


class pharmacistDetails(models.Model):
    user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE, null=True, blank=True)
    licence_image = models.FileField(default='default.jpg', upload_to='pharmacit_pics', null=True, blank=True)
    registration_image = models.FileField(default='default.jpg', upload_to='pharmacit_pics', null=True, blank=True)
    id_image = models.FileField(default='default.jpg', upload_to='pharmacit_pics', null=True, blank=True)
    tan_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.user.mobile_number   

class pharmacistStock(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, null=True, blank=True)
    meedgo_medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE, null=True, blank=True)
    manufracturing_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    pharmacist_price = models.IntegerField(default=0)
    total_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.user.mobile_number  


class pharmacistBiding(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    Pharmacist_best_price = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_biding_done = models.BooleanField(default=False)

    def __str__(self):
        return self.user.mobile_number

    class Meta:
        unique_together = ('user', 'order',)

