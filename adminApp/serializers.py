from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import *
from users.models import CustomeUser, Medicine, Profile, Order
from users.serializers import UserSerializer, OrderSerializer
from rest_framework.authtoken.models import Token
from drf_writable_nested.serializers import WritableNestedModelSerializer

User = get_user_model()

class weekOrderDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = "__all__"