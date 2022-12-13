from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import *
from users.models import CustomeUser
from users.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from drf_writable_nested.serializers import WritableNestedModelSerializer

User = get_user_model()

class pharmacistDetailsSerializer(serializers.ModelSerializer):
  user = serializers.SerializerMethodField("get_user", allow_null=True)
  class Meta:
    model = pharmacistDetails
    fields = "__all__"

  def get_user(self, obj):
    user_obj = CustomeUser.objects.get(id=obj.user.id)
    serializer = UserSerializer(user_obj, many=False)
    return serializer.data