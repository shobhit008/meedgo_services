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
from .models import Profile
from .price_scraping import One_mg, pharm_easy
from .serializers import UserProfileSerializer, UserSerializer, searchSerializer, ProfileSerializer, UserSerializer_get
import traceback


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
        "isActivated":serializer.data["isVerified"],
        "user_type":serializer.data["user_type"],
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
      profile = Profile.objects.get(user = request.user)
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
    