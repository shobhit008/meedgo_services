from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import status
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
from .models import *
from users.models import Order
from users.serializers import UserSerializer, OrderSerializer
from .serializers import *
import traceback
from meedgo_services.utils import order_number
from .permissions import *
from datetime import timedelta, datetime
from django.db.models.functions import Now
from django.utils import timezone
from django.db.models import Count
from django.db.models import F, Func, Value, CharField,Sum

# Create your views here.

class weekOrderData(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AdminAppPermission,)
  serializer_class = weekOrderDataSerializer

  def get(self,request,*args,**kwargs):
    # order_obj = Order.objects.filter(user_id = request.user.id)
    order_obj = Order.objects.filter(created__gte=datetime.now()-timedelta(days=7)).extra({'date_created' : "date(created)"}).values('date_created').annotate(created_count=Count('id'))
    res = []
    for i in order_obj:
        res.append({"date":i['date_created'], 'count':i['created_count']})

    if True:
      return Response({"data":res}, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
class monthlySaleValue(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AdminAppPermission,)
  serializer_class = weekOrderDataSerializer

  def get(self,request,*args,**kwargs):
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    year = datetime.now().year
    res = []

    for month in months:
       orders = Order.objects.filter(created__year=year, created__month=month)
       res.append({"date":f"{year}-{month}-01", "value":sum([i.total for i in orders])})

    if True:
      return Response({"data":res}, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
class monthlyCommission(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AdminAppPermission,)
  serializer_class = weekOrderDataSerializer

  def get(self,request,*args,**kwargs):
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    year = datetime.now().year
    marginPercent = 2
    res = []

    for month in months:
       orders = Order.objects.filter(created__year=year, created__month=month)
       res.append({"date":f"{year}-{month}-01", "value":sum([marginPercent*i.total/100 for i in orders])})

    if True:
      return Response({"data":res}, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)