from django.contrib import admin
from .models import PaytmTransaction

# Register your models here.

class PaytmTransactionAdmin(admin.ModelAdmin):
    """
    This class is used to display the pharmacistStock model in the admin page.
    """
    list_display = ('made_by', 'made_on', 'amount', 'order_id', 'checksum')

admin.site.register(PaytmTransaction, PaytmTransactionAdmin)