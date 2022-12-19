from django.urls import path, include
from .views import docUpdaload, pharmacistStockView, pharmacistDetailsList, pharmacistBidingView, winLossBidingCount

urlpatterns = [
    path('doc_upload/',docUpdaload.as_view(), name="doc_upload"),
    path('pharmacist_Stock/',pharmacistStockView.as_view(), name="pharmacistStock"),
    path('pharmacist_list/',pharmacistDetailsList.as_view(), name="pharmacist_list"),
    path('pharmacist_biding/',pharmacistBidingView.as_view(), name="pharmacist_biding"),
    path('win_loss_biding_count/',winLossBidingCount.as_view(), name="win_loss_biding_count"),
]