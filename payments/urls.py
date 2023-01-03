from django.urls import path
from .views import callback, initiatePayment, paymentCallback

urlpatterns = [
    path('pay/', initiatePayment.as_view(), name='pay'),
    path('callback/', paymentCallback.as_view(), name='callback'),
]