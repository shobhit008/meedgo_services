from django.urls import path, include
from .views import *

urlpatterns = [
    path('week_order_data/',weekOrderData.as_view(), name="week_order_data"),
    path('monthly_sale_value/',monthlySaleValue.as_view(), name="monthly_sale_value"),
    path('monthly_commission/',monthlyCommission.as_view(), name="monthly_commission"),
    path('transaction_count/',transactionCount.as_view(), name="transaction_count"),
]