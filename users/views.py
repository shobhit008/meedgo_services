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
from .price_scraping import One_mg
from .serializers import UserProfileSerializer, UserSerializer, searchSerializer
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

class getUserDetail(generics.CreateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    profile_obj = Profile.objects.filter(user = user)
    profile_serializer = UserProfileSerializer(profile_obj, many=True)
    serializer = UserSerializer(user)
    return Response({
        "id":serializer.data["id"],
        "name":serializer.data["name"],
        "email_address": serializer.data["email"],
        "mobile_no":serializer.data["mobile_number"],
        "isActivated":serializer.data["isVerified"],
        "user_type":serializer.data["user_type"],
        "profile_image":profile_serializer.data[0]['image'] if len(profile_serializer.data) != 0 else ""
    })


#Class based view to register user
class SearchAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = searchSerializer

  def post(self, request, *args, **kwargs):
    serch_Item = request.data
    searched_data = One_mg(serch_Item)
    return Response(searched_data, status=200)
    