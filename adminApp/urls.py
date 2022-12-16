from django.urls import path, include
from .views import *

urlpatterns = [
    path('week_order_data/',weekOrderData.as_view(), name="week_order_data"),
]