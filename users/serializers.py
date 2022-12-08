from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import CustomeUser, Profile
from rest_framework.authtoken.models import Token
from drf_writable_nested.serializers import WritableNestedModelSerializer

User = get_user_model()
#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = "__all__"

#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  Token = serializers.SerializerMethodField("get_token", allow_null=True)

  class Meta:
    model = User
    fields = ('name','email', 'mobile_number','password', 'password2',
          'first_name', 'last_name', 'Token', 'gender', 'user_type')
    extra_kwargs = {
      'first_name': {'required': False},
      'last_name': {'required': False},
      'mobile_number': {'required': True}
    }

  def get_token(self, obj):
    token, created = Token.objects.get_or_create(user=obj)
    return str(token)

  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      gender = validated_data['gender'],
      mobile_number = validated_data['mobile_number'],
      user_type = validated_data['user_type'],
      name = validated_data['name']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class  UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class searchSerializer(serializers.ModelSerializer):
  searchField = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = Profile
    fields = ('searchField',)
    extra_kwargs = {
      'searchField': {'required': True}
    }