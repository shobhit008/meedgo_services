from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import *
from users.models import CustomeUser, Medicine, Profile
from users.serializers import UserSerializer, MedicineSerializer, ProfileSerializer, UserProfileSerializer, OrderSerializer
from rest_framework.authtoken.models import Token
from drf_writable_nested.serializers import WritableNestedModelSerializer

User = get_user_model()

class pharmacistDetailsSerializer(serializers.ModelSerializer):
  user_data = serializers.SerializerMethodField("get_user", allow_null=True)
  class Meta:
    model = pharmacistDetails
    fields = "__all__"

  def get_user(self, obj):
    user_obj = CustomeUser.objects.get(id=obj.user.id)
    serializer = UserSerializer(user_obj, many=False)
    return serializer.data

class pharmacistStockSerializer(serializers.ModelSerializer):
  meedgo_medicine_details = serializers.SerializerMethodField("get_meedgo_medicine", allow_null=True)
  class Meta:
    model = pharmacistStock
    fields = "__all__"

  def get_meedgo_medicine(self, obj):
    med_obj = Medicine.objects.get(id = obj.meedgo_medicine.id)
    serializer = MedicineSerializer(med_obj, many=False)
    return serializer.data

class pharmacistDetailsDocSerializer(serializers.ModelSerializer):
  class Meta:
    model = pharmacistDetails
    fields = "__all__"



class UserPharmacistSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
  profile = serializers.SerializerMethodField("get_profile", allow_null=True)
  pharmacist_docs = serializers.SerializerMethodField("get_pharmacist_docs", allow_null=True)
  class Meta:
    model = User
    fields = "__all__"

  def get_profile(self, obj):
    profile_obj = Profile.objects.filter(user_id = obj.id)
    serializer = UserProfileSerializer(profile_obj, many=True)
    return serializer.data

  def get_pharmacist_docs(self, obj):
    pharmacist_obj = pharmacistDetails.objects.filter(user_id = obj.id)
    serializer = pharmacistDetailsDocSerializer(pharmacist_obj, many=True)
    return serializer.data

class pharmacistBidingSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
  user_data = serializers.SerializerMethodField("get_user", allow_null=True)
  order_data = serializers.SerializerMethodField("get_order", allow_null=True)
  class Meta:
    model = pharmacistBiding
    fields = "__all__"
  
  def get_user(self, obj):
    user_obj = CustomeUser.objects.get(id = obj.user.id)
    serializer = UserProfileSerializer(user_obj, many=False)
    return serializer.data

  def get_order(self, obj):
    order_obj = Order.objects.get(id = obj.order.id)
    serializer = OrderSerializer(order_obj, many=False)
    return serializer.data