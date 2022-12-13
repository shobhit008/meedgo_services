from django.urls import path, include
from .views import RegisterUserAPIView, getUserDetail, SearchAPIViewList, SearchAPIViewDict, ProfilePicView, AddressBookDetail, OrderDetail, MedicineDetail, cartDetail, userIssueDetail, userIssueDetailAdmin, searchMedicine
from django.urls import path, include
from .otp_views import getPhoneNumberRegistered, getPhoneNumberRegistered_TimeBased, getPhoneNumberRegistered_TimeBased_verify

urlpatterns = [
    path('register/',RegisterUserAPIView.as_view(), name="register"),
    # path("<phone>/", getPhoneNumberRegistered.as_view(), name="OTP Gen"),
    path("time_based/<phone>", getPhoneNumberRegistered_TimeBased.as_view(), name="OTP Gen Time Based"),
    path("time_based/verify/<phone>/<otp>", getPhoneNumberRegistered_TimeBased_verify.as_view(), name="OTP Gen Time Based verify"),
    path("get_user_details/", getUserDetail.as_view(), name="get_user_details"),
    path("Search_medicine_dict/", SearchAPIViewDict.as_view(), name="SearchAPIViewDict"),
    path("Search_medicine_list/", SearchAPIViewList.as_view(), name="SearchAPIViewList"),
    path('update_profile_pic/', ProfilePicView.as_view(), name='update_profile_pic'),
    path('Address_Book_Details/', AddressBookDetail.as_view(), name='AddressBookDetail'),
    path('make_order/', OrderDetail.as_view(), name='make_order'),
    path('medicine/', MedicineDetail.as_view(), name='medicine'),
    path('cart/', cartDetail.as_view(), name='cart'),
    path('user_Issue/', userIssueDetail.as_view(), name='userIssueDetail'),
    path('user_Issue_admin/', userIssueDetailAdmin.as_view(), name='userIssueDetailAdmin'),
    path('search_meedgo_medicine/', searchMedicine.as_view(), name='search_medicine'),
]