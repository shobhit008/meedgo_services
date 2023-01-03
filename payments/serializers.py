from .models import PaytmTransaction

from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
  order_number = serializers.CharField(write_only=True, required=True)
  amount = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = PaytmTransaction
    fields = ('order_number','amount')
    extra_kwargs = {
      'order_number': {'required': True},
      'amount': {'required': True}
    }