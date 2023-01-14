from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import PaytmTransaction
from .paytm import *
import requests
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomeUser, Order
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import status
from .serializers import *
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
import json
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser

# import PaytmChecksum
#Class based view to register user
class initiatePayment(generics.CreateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  serializer_class = TransactionSerializer

  def post(self, request, *args, **kwargs):
    order_obj = Order.objects.get(order_number = request.data['order_number'])
    transaction = PaytmTransaction.objects.create(made_by=request.user, amount=request.data['amount'], order_id= order_obj)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    ###############################################################################
    paytmParams = dict()
    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : settings.PAYTM_MERCHANT_ID,
        "websiteName"   : "PAYTM_WEBSITE",
        "orderId"       : str(transaction.order_id.order_number),
        "callbackUrl"   : f"https://securegw-stage.paytm.in/theia/paytmCallback?ORDER_ID={str(transaction.order_id.order_number)}",
        "txnAmount"     : {
            "value"     : str(transaction.amount),
            "currency"  : "INR",
        },
        "userInfo"      : {
            "custId"    : str(transaction.made_by.mobile_number),
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = generateSignature(json.dumps(paytmParams["body"]), settings.PAYTM_SECRET_KEY)

    paytmParams["head"] = {
        "signature"    : checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={settings.PAYTM_MERCHANT_ID}&orderId={str(transaction.order_id.order_number)}"

    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    transaction.checksum = f'''{response}'''
    transaction.save()
    return Response(response, status=200)

    ###############################################################################

    # params = (
    #     ('MID', settings.PAYTM_MERCHANT_ID),
    #     ('ORDER_ID', str(transaction.order_id.order_number)),
    #     ('CUST_ID', str(transaction.made_by.mobile_number)),
    #     ('TXN_AMOUNT', str(transaction.amount)),
    #     ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
    #     ('WEBSITE', settings.PAYTM_WEBSITE),
    #     # ('EMAIL', request.user.email),
    #     # ('MOBILE_N0', '9911223388'),
    #     ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
    #     ('CALLBACK_URL', 'http://127.0.0.1:8000/payment/callback/'),
    #     # ('PAYMENT_MODE_ONLY', 'NO'),
    # )

    # paytm_params = dict(params)
    # checksum = generate_checksum(paytm_params, merchant_key)

    # transaction.checksum = checksum
    # transaction.save()

    # paytm_params['CHECKSUMHASH'] = checksum
    # print('SENT: ', checksum)
    # return Response(paytm_params, status=200)


# def initiate_payment(request):
#     if request.method == "GET":
#         return render(request, 'payments/pay.html')
#     # try:
#     #     username = request.POST['username']
#     #     password = request.POST['password']
#     #     amount = int(request.POST['amount'])
#     #     user = authenticate(request, username=username, password=password)
#     #     if user is None:
#     #         raise ValueError
#     #     auth_login(request=request, user=user)
#     # except:
#     #     return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})
#     user = CustomeUser.objects.get(id = 1)
#     transaction = PaytmTransaction.objects.create(made_by=user, amount=100)
#     transaction.save()
#     merchant_key = settings.PAYTM_SECRET_KEY

#     params = (
#         ('MID', settings.PAYTM_MERCHANT_ID),
#         ('ORDER_ID', str(transaction.order_id.order_number)),
#         ('CUST_ID', str(transaction.made_by.email)),
#         ('TXN_AMOUNT', str(transaction.amount)),
#         ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
#         ('WEBSITE', settings.PAYTM_WEBSITE),
#         # ('EMAIL', request.user.email),
#         # ('MOBILE_N0', '9911223388'),
#         ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
#         ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
#         # ('PAYMENT_MODE_ONLY', 'NO'),
#     )

#     paytm_params = dict(params)
#     checksum = generate_checksum(paytm_params, merchant_key)

#     transaction.checksum = checksum
#     transaction.save()

#     paytm_params['CHECKSUMHASH'] = checksum
#     print('SENT: ', checksum)
#     return render(request, 'payments/redirect.html', context=paytm_params)


#Class based view to register user
class paymentCallback(generics.CreateAPIView):
  '''
  Put all the payload from paytm pay api
  '''
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  serializer_class = TransactionSerializer

  def post(self, request, *args, **kwargs):
    received_data = dict(request.data)
    paytm_params = {}
    paytm_checksum = ""#received_data['CHECKSUMHASH']
    STATUS= ""
    for key, value in received_data.items():
        if key == 'STATUS':
            STATUS = value
        if key == 'CHECKSUMHASH':
            paytm_checksum = value
        else:
            paytm_params[key] = str(value)
    try:
        order_obj = PaytmTransaction.objects.get(order_id__order_number = received_data['ORDER_ID'])
    except:
        received_data['msg'] = "something went wrong"
        return Response(received_data, status=status.HTTP_400_BAD_REQUEST)

    if STATUS == "TXN_SUCCESS":
        received_data['msg'] = "Payment successful"
        order_obj.status = "successfull"
        order_obj.save()
        return Response(received_data, status=status.HTTP_200_OK)
    else:
        received_data['msg'] = "Payment Failed"
        order_obj.status = "failed"
        order_obj.save()
        return Response(received_data, status=status.HTTP_400_BAD_REQUEST)


    # Verify checksum
    is_valid_checksum=""
    try:
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
    except:
        pass

    if is_valid_checksum:
        received_data['msg'] = "Checksum Matched"
    else:
        received_data['msg'] = "Checksum Mismatched"
        return Response(received_data, status=status.HTTP_200_OK)
    
    return Response(received_data, status=200)









@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)