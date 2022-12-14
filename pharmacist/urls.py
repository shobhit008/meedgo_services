from django.urls import path, include
from .views import docUpdaload, pharmacistStockView, pharmacistDetailsList

urlpatterns = [
    path('doc_upload/',docUpdaload.as_view(), name="doc_upload"),
    path('pharmacist_Stock/',pharmacistStockView.as_view(), name="pharmacistStock"),
    path('pharmacist_list/',pharmacistDetailsList.as_view(), name="pharmacist_list"),
]