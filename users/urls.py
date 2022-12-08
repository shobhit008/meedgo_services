from django.urls import path, include
from .views import RegisterUserAPIView, getUserDetail, SearchAPIView
from django.urls import path, include
from .otp_views import getPhoneNumberRegistered, getPhoneNumberRegistered_TimeBased, getPhoneNumberRegistered_TimeBased_verify

urlpatterns = [
    path('register/',RegisterUserAPIView.as_view(), name="register"),
    # path("<phone>/", getPhoneNumberRegistered.as_view(), name="OTP Gen"),
    path("time_based/<phone>", getPhoneNumberRegistered_TimeBased.as_view(), name="OTP Gen Time Based"),
    path("time_based/verify/<phone>/<otp>", getPhoneNumberRegistered_TimeBased_verify.as_view(), name="OTP Gen Time Based verify"),
    path("get_user_details/", getUserDetail.as_view(), name="get_user_details"),
    path("Search_medicine/", SearchAPIView.as_view(), name="SearchAPIView"),
]