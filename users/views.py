from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import status
from .serializers import RegisterSerializer
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
from .models import Profile, AddressBook, Order
from .price_scraping import One_mg, pharm_easy
from .serializers import UserProfileSerializer, UserSerializer, searchSerializer, ProfileSerializer, UserSerializer_get, AddressBookSerializer, OrderSerializer
import traceback
from meedgo_services.utils import order_number


User = get_user_model()

# Create your views here.
#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class getUserDetail(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  serializer_class = UserSerializer_get
  
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    profile_obj = Profile.objects.filter(user = user)
    profile_serializer = UserProfileSerializer(profile_obj, many=True)
    serializer = UserSerializer_get(user)
    return Response({
        "id":serializer.data["id"],
        "name":serializer.data["name"],
        "email_address": serializer.data["email"],
        "mobile_no":serializer.data["mobile_number"],
        "whatapp_mobile_number":serializer.data["whatapp_mobile_number"],
        "data_of_birth":serializer.data["birth_date"],
        "isActivated":serializer.data["isVerified"],
        "user_type":serializer.data["user_type"],
        "gender": serializer.data["gender"],
        "age": serializer.data["age"],
        "profile_image":profile_serializer.data[0]['image'] if len(profile_serializer.data) != 0 else ""
    })
  
  def update(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    profile_obj = Profile.objects.filter(user = user)
    user_serializer = UserSerializer(user, data=request.data, partial=False)
    if user_serializer.is_valid():
      user_serializer.save()

    res = {
      "msg":"Profile updated successfully",
    }
    return Response(res, status=status.HTTP_201_CREATED)


#Class based view to register user
class SearchAPIViewDict(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = searchSerializer

  def post(self, request, *args, **kwargs):
    searched_data = {}
    serch_Item = request.data
    onemg_searched_data = One_mg(serch_Item)
    pharm_easy_data = pharm_easy(serch_Item)
    searched_data.update({"one_mg":onemg_searched_data, "pharm_easy":pharm_easy_data})
    return Response(searched_data, status=200)

#Class based view to register user
class SearchAPIViewList(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = searchSerializer

  def post(self, request, *args, **kwargs):
    searched_data = {}
    serch_Item = request.data
    onemg_searched_data = One_mg(serch_Item, True)
    pharm_easy_data = pharm_easy(serch_Item, True)
    searched_data.update({"one_mg":onemg_searched_data, "pharm_easy":pharm_easy_data})
    return Response(searched_data, status=200)


class ProfilePicView(generics.CreateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  parser_classes = (MultiPartParser, FormParser)
  serializer_class = ProfileSerializer

  def post(self, request, *args, **kwargs):
      profile, created = Profile.objects.get_or_create(user = request.user)
      file_serializer = ProfileSerializer(profile, data=request.data, partial=True)
      if file_serializer.is_valid():
          file_serializer.save()
          res = {
              'image':file_serializer.data['image'],
              'msg':'updated successfully',
              'code':status.HTTP_201_CREATED
          }
          return Response(res, status=status.HTTP_201_CREATED)
      else:
          res = {
              'msg':'invalide input',
              'code':status.HTTP_400_BAD_REQUEST
          }
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressBookDetail(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  serializer_class = AddressBookSerializer
  
  def get(self,request,*args,**kwargs):
    address_book_obj = AddressBook.objects.filter(user=request.user)
    serializer = AddressBookSerializer(instance=address_book_obj, many=True)
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
      serializer = AddressBookSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          res = {
              'data':serializer.data,
              'msg':'Address updated successfully',
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
      AddressBook_id = AddressBook.objects.get(id=request.data['id'])
      Address_serializer = AddressBookSerializer(AddressBook_id, data=request.data, partial=True)
      if Address_serializer.is_valid():
        Address_serializer.save()

      res = {
        "msg":"Profile updated successfully",
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  serializer_class = OrderSerializer
  
  def get(self,request,*args,**kwargs):
    address_book_obj = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(instance=address_book_obj, many=True)
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
      request.data["order_number"] = order_number(request.user.id)
      serializer = OrderSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          res = {
              'data':serializer.data,
              'msg':'Address updated successfully',
              'code':status.HTTP_201_CREATED
          }
          return Response(res, status=status.HTTP_201_CREATED)
      else:
          res = {
              'msg':'invalide input',
              'code':status.HTTP_400_BAD_REQUEST
          }
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  # def update(self,request,*args,**kwargs):
  #   try:
  #     AddressBook_id = Order.objects.get(id=request.data['id'])
  #     Address_serializer = OrderSerializer(AddressBook_id, data=request.data, partial=True)
  #     if Address_serializer.is_valid():
  #       Address_serializer.save()

  #     res = {
  #       "msg":"Profile updated successfully",
  #     }
  #     return Response(res, status=status.HTTP_200_OK)
  #   except:
  #     res = {
  #       "msg":"something went wrong",
  #     }
  #     return Response(res, status=status.HTTP_400_BAD_REQUEST)