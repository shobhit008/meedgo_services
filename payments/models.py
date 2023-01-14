from django.db import models
from django.contrib.auth import get_user_model
from users.models import Order

User = get_user_model()

class PaytmTransaction(models.Model):
    STATUS = (
        ('successfull', 'successfull'),
        ('failed', 'failed'),
        ('', ''),
    )
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.ForeignKey(Order,on_delete=models.DO_NOTHING, blank=True, null=True, related_name="transaction_order_id") #models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='')

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
