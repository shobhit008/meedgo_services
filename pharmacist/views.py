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
from users.serializers import UserSerializer
from .serializers import pharmacistDetailsSerializer, pharmacistStockSerializer, UserPharmacistSerializer, pharmacistBidingSerializer
import traceback
from meedgo_services.utils import order_number
from .permissions import PharmacistPermission
from datetime import timedelta
from django.db.models.functions import Now
from django.utils import timezone

# Create your views here.
class docUpdaload(UpdateAPIView):
  # authentication_classes = (TokenAuthentication,)
  # permission_classes = (IsAuthenticated,)
  parser_classes = (MultiPartParser, FormParser)
  serializer_class = pharmacistDetailsSerializer

  def get(self,request,*args,**kwargs):
    cart_obj = pharmacistDetails.objects.all()
    serializer = self.serializer_class(instance=cart_obj, many=True)
    if True:
      return Response(serializer.data, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data)
    if request.data['user']:
      user = CustomeUser.objects.get(id=request.data['user'])
      if user.is_active:
          res = {
              'msg':'Something went worng',
              'code':status.HTTP_400_BAD_REQUEST
          }

          return Response(res, status=status.HTTP_400_BAD_REQUEST)

      else:
        pass
        # user.is_active = True
        # user.save()

      if serializer.is_valid():
          serializer.save()
          res = {
              'data':serializer.data,
              'msg':'Document uploaded successfully',
              'code':status.HTTP_201_CREATED
          }
          return Response(res, status=status.HTTP_201_CREATED)
      else:
          res = {
              'msg':'invalide input',
              'code':status.HTTP_400_BAD_REQUEST
          }
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
          res = {
              'msg':'Something went worng',
              'code':status.HTTP_400_BAD_REQUEST
          }
          return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def update(self,request,*args,**kwargs):
    try:
      user_issue_id = CustomeUser.objects.get(id=request.data['user'])
      request.data.pop('user')
      pharmacist_serializer = self.serializer_class(user_issue_id, data=request.data, partial=True)
      if pharmacist_serializer.is_valid():
        pharmacist_serializer.save()

      res = {
          'data':pharmacist_serializer.data,
          'msg':'pharmacist details updated successfully',
          'code':status.HTTP_201_CREATED
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
class pharmacistStockView(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (PharmacistPermission,)
  serializer_class = pharmacistStockSerializer

  def get(self,request,*args,**kwargs):
    stock_obj = pharmacistStock.objects.filter(user_id = request.user.id)
    serializer = self.serializer_class(instance=stock_obj, many=True)
    if True:
      return Response(serializer.data, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def post(self, request, *args, **kwargs):
      request.data['user'] = request.user.id
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
          serializer.save()
          res = {
              'data':serializer.data,
              'msg':'Medicine Added successfully',
              'code':status.HTTP_201_CREATED
          }
          return Response(res, status=status.HTTP_201_CREATED)
      else:
          res = {
              'msg':'invalide input',
              'code':status.HTTP_400_BAD_REQUEST
          }
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self,request,*args,**kwargs):
    try:
      pharmacistStock_obj = pharmacistStock.objects.get(user_id=request.user.id, id=request.data['id'])
      request.data.pop('user')
      pharmacist_serializer = self.serializer_class(pharmacistStock_obj, data=request.data, partial=True)
      if pharmacist_serializer.is_valid():
        pharmacist_serializer.save()

      res = {
          'data':pharmacist_serializer.data,
          'msg':'Data updated successfully',
          'code':status.HTTP_201_CREATED
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

class pharmacistDetailsList(UpdateAPIView):
  '''
  For update method please add below payload
  {
  "id":Integer,
  "is_approved":true
  }
  '''
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  serializer_class = UserPharmacistSerializer

  def get(self,request,*args,**kwargs):
    pharmacist_obj = CustomeUser.objects.filter(user_type = "Pharmacists")
    serializer = self.serializer_class(instance=pharmacist_obj, many=True)
    if True:
      return Response(serializer.data, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def update(self,request,*args,**kwargs):
    try:
      user_obj = CustomeUser.objects.get(id = request.data.get("id"))
      if request.data.get("is_approved"):
        user_obj.is_active = True
        user_obj.save()
      else:
        user_obj.is_active = False
        user_obj.save()

      res = {
          'msg':'updated successfully',
          'code':status.HTTP_201_CREATED
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


class pharmacistBidingView(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (PharmacistPermission,)
  serializer_class = pharmacistBidingSerializer

  def get(self,request,*args,**kwargs):
    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    one_hour_later = this_hour + timedelta(hours=2)

    booked_order_obj = Order.objects.filter(status="initiated", created__gt=Now()-timedelta(hours=2)).order_by('-created')
    bulk_create_list = [pharmacistBiding(user = request.user, order = orderItem,) for orderItem in booked_order_obj]
    bulk_create_obj = []
    # bulk_create_obj = pharmacistBiding.objects.bulk_create(bulk_create_list)
    for i in bulk_create_list:
      try:
         obkj = pharmacistBiding.objects.bulk_create(bulk_create_list)
         bulk_create_obj.append(obkj[0])
      except:
        continue

    biding_log = pharmacistBiding.objects.filter(is_biding_done = False).order_by('-created')
    serializer = self.serializer_class(instance=biding_log, many=True)
    if True:
      return Response(serializer.data, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def update(self,request,*args,**kwargs):
    try:
      bid_obj = pharmacistBiding.objects.get(id = request.data.get('id'))
      bid_obj.Pharmacist_best_price = request.data.get('Pharmacist_best_price')
      bid_obj.quantity = request.data.get('quantity')
      bid_obj.is_biding_done = True
      bid_obj.save()

      res = {
          'msg':'Biding posted successfully',
          'code':status.HTTP_201_CREATED
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)