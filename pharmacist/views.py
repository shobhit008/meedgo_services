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
from .serializers import pharmacistDetailsSerializer
import traceback
from meedgo_services.utils import order_number

# Create your views here.
class docUpdaload(UpdateAPIView):
  # authentication_classes = (TokenAuthentication,)
  # permission_classes = (IsAuthenticated,)
  parser_classes = (MultiPartParser, FormParser)
  serializer_class = pharmacistDetailsSerializer

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
        user.is_active = True
        user.save()

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
