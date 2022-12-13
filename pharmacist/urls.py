from django.urls import path, include
from .views import docUpdaload, pharmacistStockView

urlpatterns = [
    path('doc_upload/',docUpdaload.as_view(), name="doc_upload"),
    path('pharmacist_Stock/',pharmacistStockView.as_view(), name="pharmacistStock"),
]