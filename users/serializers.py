from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import CustomeUser, Profile, AddressBook,Order, Medicine, Cart, orderMedicineData, userIssue ,orderCartData, feedback
from pharmacist.models import pharmacistBiding
from rest_framework.authtoken.models import Token
from drf_writable_nested.serializers import WritableNestedModelSerializer

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('image',)

class UserSerializer_get(WritableNestedModelSerializer, serializers.ModelSerializer):
  class Meta:
    model = User
    fields = "__all__"

#Serializer to Get User Details using Django Token Authentication
class UserSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
  class Meta:
    model = User
    fields = "__all__"

  def get_fields(self):
      fields = super().get_fields()

      exclude_fields = self.context.get('exclude_fields', ["mobile_number","groups", "user_permissions", "password"])
      for field in exclude_fields:
        if field in ["mobile_number","groups", "user_permissions", "password"]:
          fields.pop(field, default=None)
        else:
          fields.pop(field, default=None)

      return fields


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
    fields = ('id','name','email', 'mobile_number','password', 'password2',
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
    if validated_data['user_type'] == "Pharmacists":
      user = User.objects.create(
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        gender = validated_data['gender'],
        mobile_number = validated_data['mobile_number'],
        user_type = validated_data['user_type'],
        name = validated_data['name'],
        is_active = False
      )
    else:
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

class AddressBookSerializer(serializers.ModelSerializer):
  class Meta:
    model = AddressBook
    fields = "__all__"

class orderMedicineDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = orderMedicineData
    fields = "__all__"



class MedicineSerializer(serializers.ModelSerializer):
  class Meta:
    model = Medicine
    fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
  cart = serializers.SerializerMethodField("get_cart", allow_null=True)
  user_details = serializers.SerializerMethodField("get_user", allow_null=True)
  phamacist_details = serializers.SerializerMethodField("get_phamacist", allow_null=True)
  phamacist_lat_long = serializers.SerializerMethodField("get_phamacist_lat_log", allow_null=True)
  add_cart = serializers.ListField(allow_null=True, required=False)
  class Meta:
    model = Order
    fields = "__all__"

  def get_user(self, obj):
    userObj = User.objects.get(id=obj.user.id)
    serializer = UserSerializer(userObj, many=False)
    return serializer.data

  def get_phamacist(self, obj):
    if obj.phamacist_data:
      userObj = User.objects.get(id=obj.phamacist_data.id)
      serializer = UserSerializer(userObj, many=False)
      return serializer.data
    else:
      return {}

  def get_phamacist_lat_log(self, obj):
    if obj.phamacist_data:
      userObj = User.objects.get(id=obj.phamacist_data.id)
      serializer = UserSerializer(userObj, many=False)
      pharma_adddress = AddressBook.objects.filter(user_id=obj.phamacist_data.id, is_default=True)
      if pharma_adddress.count()>0:
        lat = pharma_adddress[0].lat
        long = pharma_adddress[0].long
      else:
        lat = ""
        long = ""

      return {"lat":lat, "long":long}
    else:
      return {}

  def get_cart(self, obj):
    orderCart = orderCartData.objects.filter(order = obj)
    cartList = [i.cart.id for i in orderCart if i.cart]
    oderedCart = Cart.objects.filter(id__in=cartList)
    serializer = CartSerializer(oderedCart, many=True)
    # serializer = orderMedicineDataSerializer(orderMedicine, many=True)
    return serializer.data

class CartSerializer(serializers.ModelSerializer):
  medicenes_details = serializers.SerializerMethodField("get_mediciens", allow_null=True)
  class Meta:
    model = Cart
    fields = "__all__"

  def get_mediciens(self, obj):
    oderedMedicenes = Medicine.objects.get(id=obj.medicine.id)
    serializer = MedicineSerializer(oderedMedicenes, many=False)
    # serializer = orderMedicineDataSerializer(orderMedicine, many=True)
    return serializer.data

class userIssueSerializer(serializers.ModelSerializer):
  class Meta:
    model = userIssue
    fields = "__all__"

class userIssueSerializer_admin(serializers.ModelSerializer):
  user_name = serializers.CharField(source='user.name')
  phone_number = serializers.CharField(source='user.mobile_number')
  class Meta:
    model = userIssue
    fields = "__all__"

class searchMedicineSerializer(serializers.ModelSerializer):
  searchField = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = Profile
    fields = ('searchField',)
    extra_kwargs = {
      'searchField': {'required': True}
    }

class orderBidingSerializer(serializers.ModelSerializer):
  user_details = serializers.SerializerMethodField("get_user", allow_null=True)
  phamacist_lat_long = serializers.SerializerMethodField("get_phamacist_lat_log", allow_null=True)
  order_details = serializers.SerializerMethodField("get_order", allow_null=True)
  class Meta:
    model = pharmacistBiding
    fields = "__all__"

  def get_user(self, obj):
    userObj = User.objects.get(id=obj.user.id)
    serializer = UserSerializer(userObj, many=False)
    # serializer = orderMedicineDataSerializer(orderMedicine, many=True)
    return serializer.data
  
  def get_order(self, obj):
    orderObj = Order.objects.get(id = obj.order.id)
    serializer = OrderSerializer(orderObj, many=False)
    return serializer.data

  def get_phamacist_lat_log(self, obj):
    if obj.user:
      userObj = User.objects.get(id=obj.user.id)
      serializer = UserSerializer(userObj, many=False)
      pharma_adddress = AddressBook.objects.filter(user_id=obj.user.id, is_default=True)
      if pharma_adddress.count()>0:
        lat = pharma_adddress[0].lat
        long = pharma_adddress[0].long
      else:
        lat = ""
        long = ""

      return {"lat":lat, "long":long}
    else:
      return {}

class feedbackSerializer(serializers.ModelSerializer):
  order_number = serializers.SerializerMethodField("get_order_number", allow_null=True)
  class Meta:
    model = feedback
    fields = "__all__"
  
  def get_order_number(self, obj):
    return obj.order.order_number