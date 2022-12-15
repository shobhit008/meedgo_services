from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import CustomeUser, Profile, AddressBook,Order, Medicine, Cart, orderMedicineData, userIssue
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
  medicenes = serializers.SerializerMethodField("get_mediciens", allow_null=True)
  add_medicines = serializers.ListField(allow_null=True, required=False)
  class Meta:
    model = Order
    fields = "__all__"

  def get_mediciens(self, obj):
    orderMedicine = orderMedicineData.objects.filter(order = obj)
    medicineIdList = [i.medicine.id for i in orderMedicine]
    oderedMedicenes = Medicine.objects.filter(id__in=medicineIdList)
    serializer = MedicineSerializer(oderedMedicenes, many=True)
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