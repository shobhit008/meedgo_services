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
from .models import Profile, AddressBook, Order, Medicine, Cart, orderMedicineData, userIssue, feedback
from pharmacist.models import pharmacistBiding, WinBid
from .price_scraping import One_mg, pharm_easy, flipkart_health
from .serializers import UserProfileSerializer, UserSerializer, searchSerializer, ProfileSerializer, UserSerializer_get, AddressBookSerializer, OrderSerializer, MedicineSerializer, CartSerializer, userIssueSerializer, userIssueSerializer_admin, searchMedicineSerializer, orderCartData, orderBidingSerializer, feedbackSerializer
import traceback
from django.db.models import Q
from meedgo_services.utils import order_number
from rest_framework.pagination import PageNumberPagination
from .constants import *


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
    flipkart_health_data = flipkart_health(serch_Item)
    searched_data.update({"one_mg":onemg_searched_data, "pharm_easy":pharm_easy_data, "flipkart_health":flipkart_health_data})
    return Response(searched_data, status=200)

#Class based view to register user
class SearchAPIViewDict_one_mg(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = searchSerializer

  def post(self, request, *args, **kwargs):
    searched_data = {}
    serch_Item = request.data
    onemg_searched_data = One_mg(serch_Item)
    searched_data.update({"one_mg":onemg_searched_data})
    return Response(searched_data, status=200)

#Class based view to register user
class SearchAPIViewDict_pharm_easy(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = searchSerializer

  def post(self, request, *args, **kwargs):
    searched_data = {}
    serch_Item = request.data
    pharm_easy_data = pharm_easy(serch_Item)
    searched_data.update({"pharm_easy":pharm_easy_data})
    return Response(searched_data, status=200)

#Class based view to register user
class SearchAPIViewDict_flipkart(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = searchSerializer

  def post(self, request, *args, **kwargs):
    searched_data = {}
    serch_Item = request.data
    flipkart_health_data = flipkart_health(serch_Item)
    searched_data.update({"flipkart_health":flipkart_health_data})
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
    flipkart_health_data = flipkart_health(serch_Item, True)
    searched_data.update({"one_mg":onemg_searched_data, "pharm_easy":pharm_easy_data, "flipkart_health":flipkart_health_data})
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

def setDefaultAddr(request):
  address_book_obj = AddressBook.objects.filter(user=request.user)
  for i in address_book_obj:
    i.is_default=False
    i.save()

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
          if request.data.get("is_default", False):
              setDefaultAddr(request)
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
        if request.data.get("is_default"):
            setDefaultAddr(request)
        Address_serializer.save()

      res = {
        "msg":"Address updated successfully",
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, format=None):
    try:
      event = AddressBook.objects.get(id = request.data['id'])
      event.delete()
      res = {
        "msg":"Address deleted successfully",
      }
      return Response(res, status=status.HTTP_204_NO_CONTENT)

    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


def createOrderCart(user, data, order_id):
  if type(data) == str:
    data = [str(i) for i in data.split(",")]
  for i in data:
    orderCartData.objects.create(
      order_id = order_id,
      cart_id = i
      )
    # cart_obj = Cart.objects.get(id = i)
    # cart_obj.is_order_placed = True
    # cart_obj.save()
  return True



class OrderDetail(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  parser_classes = (MultiPartParser, FormParser)
  serializer_class = OrderSerializer
  
  def get(self,request,*args,**kwargs):
    address_book_obj = Order.objects.filter(user=request.user, status__in = ['in transition', 'out for delivery', 'delivered'])
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
      if request.data.get("add_cart"):
        add_cart = request.data.get("add_cart")
        try:
          request.data.pop("add_cart")
          requestData = request.data
        except:
          requestData = request.data.dict()
          requestData.pop("add_cart")
      requestData['user'] = request.user.id
      requestData["order_number"] = order_number(request.user.id)
      serializer = OrderSerializer(data=requestData)
      if serializer.is_valid():
          serializer.save()
          createOrderCart(request.user, add_cart, serializer.data['id'])
          res = {
              'data':serializer.data,
              'msg':'Order created successfully',
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
      order_obj = Order.objects.get(order_number =request.data['order_number'])
      order_serializer = OrderSerializer(order_obj, data=request.data, partial=True)
      if order_serializer.is_valid():
        order_serializer.save()

      res = {
        "msg":"Order updated successfully",
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


class MedicineDetail(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  parser_classes = (MultiPartParser, FormParser)
  serializer_class = MedicineSerializer

  def get(self,request,*args,**kwargs):
    medicine_obj = Medicine.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(medicine_obj, request)
    serializer = self.serializer_class(instance=result_page, many=True)
    if True:
      return paginator.get_paginated_response(serializer.data)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def post(self, request, *args, **kwargs):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
          serializer.save()
          res = {
              'data':serializer.data,
              'msg':'Medicine Added successfully',
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
      medicine_id = Medicine.objects.get(name=request.data['name'])
      medicine_serializer = MedicineSerializer(medicine_id, data=request.data, partial=True)
      if medicine_serializer.is_valid():
        medicine_serializer.save()

      res = {
        "msg":"Medicine Details updated successfully",
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


class cartDetail(UpdateAPIView):
  '''
  For Delete User below Formate
  {
      "id":integer
  }
  '''
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  # parser_classes = (MultiPartParser, FormParser)
  serializer_class = CartSerializer

  def get(self,request,*args,**kwargs):
    cart_obj = Cart.objects.filter(user_id = request.user.id, is_order_placed=False)
    serializer = self.serializer_class(instance=cart_obj, many=True)
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
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
          serializer.save()
          res = {
              'data':serializer.data,
              'msg':'Cart Added successfully',
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
      cart_id = Cart.objects.get(id=request.data['id'])
      request.data.pop("user")
      cart_serializer = CartSerializer(cart_id, data=request.data, partial=True)
      if cart_serializer.is_valid():
        cart_serializer.save()

      res = {
        "msg":"Cart Details updated successfully",
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, format=None):
    try:
      orderCartData_obj = orderCartData.objects.filter(cart_id = request.data['id'])
      for i in orderCartData_obj:
        i.cart_id = ""
        i.save()
      event = Cart.objects.get(id = request.data['id'])
      event.delete()
      res = {
        "msg":"Item deleted successfully",
      }
      return Response(res, status=status.HTTP_204_NO_CONTENT)

    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)



class userIssueDetail(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  # parser_classes = (MultiPartParser, FormParser)
  serializer_class = userIssueSerializer

  def get(self,request,*args,**kwargs):
    cart_obj = userIssue.objects.filter(user_id = request.user.id)  
    serializer = self.serializer_class(instance=cart_obj, many=True)
    if True:
      return Response(serializer.data, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def post(self, request, *args, **kwargs):
      request.data['issue_number'] = order_number(request.user.id, id_type = "Issue_")
      request.data['user'] = request.user.id
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
          serializer.save()
          res = {
              'data':serializer.data,
              'msg':'Issue registed successfully',
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
      user_issue_id = userIssue.objects.get(issue_number=request.data['issue_number'])
      medicine_serializer = self.serializer_class(user_issue_id, data=request.data, partial=True)
      if medicine_serializer.is_valid():
        medicine_serializer.save()

      res = {
          'data':medicine_serializer.data,
          'msg':'Issue Updated successfully',
          'code':status.HTTP_201_CREATED
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


class userIssueDetailAdmin(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  # parser_classes = (MultiPartParser, FormParser)
  serializer_class = userIssueSerializer

  def get(self,request,*args,**kwargs):
    cart_obj = userIssue.objects.all()  
    serializer = userIssueSerializer_admin(instance=cart_obj, many=True)
    if True:
      return Response(serializer.data, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)

  def update(self,request,*args,**kwargs):
    try:
      issue_obj = userIssue.objects.get(issue_number = request.data.get("issue_number"))
      limited_Data = {
        "issue_number": request.data.get("issue_number"),
        "comments": request.data.get("issue_number"),
        "status": request.data.get("status"),
      }
      issue_serializer = self.serializer_class(issue_obj, data=limited_Data, partial=True)
      if issue_serializer.is_valid():
        issue_serializer.save()

      res = {
          'data':issue_serializer.data,
          'msg':'Issue Updated successfully',
          'code':status.HTTP_201_CREATED
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


class searchMedicine(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = searchSerializer

  def post(self, request, *args, **kwargs):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    searched_data = {}
    serch_Item = request.data
    searched_data = serch_Item['searchField'].split(",")
    data_To_search = [i.strip() for i in searched_data]
    query = Q()
    for entry in data_To_search:
        query = query | Q(name__contains=entry)
    find_med_obj = Medicine.objects.filter(query)
    result_page = paginator.paginate_queryset(find_med_obj, request)
    med_obj = MedicineSerializer(result_page, many=True)

    return paginator.get_paginated_response(med_obj.data)

def pharmacist_book_order(bid_obj):
  order_obj = Order.objects.get(order_number = bid_obj.order.order_number)
  order_obj.phamacist_data = bid_obj.user
  order_obj.status = "in transition"
  order_obj.save()
  
  # this is to mark orderd cart
  cart_obj = orderCartData.objects.filter(order__order_number = order_obj.order_number)
  for i in cart_obj:
    cart_obj = Cart.objects.get(id = i.cart_id)
    cart_obj.is_order_placed = True
    cart_obj.save()

  return order_obj

class getBidderList(UpdateAPIView):
  '''
  Customer to select a bid use put request of this api and send request in below format
  {
  "id":integer
  } 
  '''
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  serializer_class = orderBidingSerializer

  def get(self,request,*args,**kwargs):
    initialtedOrder = Order.objects.filter(user_id=request.user.id, status = "initiated").first()
    all_initiated_orders = [i.order_number for i in [initialtedOrder]]
    pharmacistBiding_obj = pharmacistBiding.objects.filter(order__order_number__in = all_initiated_orders, is_biding_done=True)
    serializer = self.serializer_class(instance=pharmacistBiding_obj, many=True)
    if True:
      return Response({"data":serializer.data}, status=status.HTTP_200_OK)

    else:
      res = {
          'msg':'something went worng',
          'code':status.HTTP_400_BAD_REQUEST
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


  def update(self,request,*args,**kwargs):
    try:
      # this code is for winner
      bid_obj = pharmacistBiding.objects.get(id = request.data.get('id'))
      bid_obj.is_biding_win = "win"
      bid_obj.save()

      pharmacist_book_order(bid_obj)
      
      # this code is for losser
      bid_obj_losser = pharmacistBiding.objects.filter(order__order_number = bid_obj.order.order_number, is_biding_done = True, is_biding_win = 'in transition')
      bid_obj_losser.update(is_biding_win='loss')

      bid_obj.is_biding_done = True
      bid_obj.save()

      data  = self.serializer_class(instance=bid_obj, many=False)

      res = {
          'msg':'order confirmed',
          'code':status.HTTP_201_CREATED,
          'data':data.data
      }
      return Response(res, status=status.HTTP_200_OK)
    except:
      res = {
        "msg":"something went wrong",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


class orderFeedback(UpdateAPIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  serializer_class = feedbackSerializer

  def post(self,request,*args,**kwargs):
    try:
      reqData = request.data
      feedback_obj, created = feedback.objects.get_or_create(order__id = reqData['order'])
      if created:
        feedback_obj.order_id = reqData.get("order", 0)
        feedback_obj.staff_friendliness = reqData.get("staff_friendliness", 0)
        feedback_obj.online_delivery = reqData.get("online_delivery", 0)
        feedback_obj.pharmacist_knowledge = reqData.get("pharmacist_knowledge", 0)
        feedback_obj.home_delivery = reqData.get("home_delivery", False)
        feedback_obj.within_quotation = reqData.get("within_quotation", False)
        feedback_obj.discount = reqData.get("discount", 0)
        feedback_obj.save()

      data  = self.serializer_class(instance=feedback_obj, many=False)
      res = {
          'msg':'Order feedback',
          'code':status.HTTP_200_OK,
          'data':data.data
      }
      return Response(res, status=status.HTTP_200_OK)

    except:
      res = {
          'msg':'something went wrong',
          'code':status.HTTP_400_BAD_REQUEST,
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)


    



    
