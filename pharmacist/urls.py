from django.urls import path, include
from .views import docUpdaload, pharmacistStockView, pharmacistDetailsList, pharmacistBidingView, winLossBidingCount, pharmacistOrdarTracking, pharmacistMissedOrdarTracking

urlpatterns = [
    path('doc_upload/',docUpdaload.as_view(), name="doc_upload"),
    path('pharmacist_Stock/',pharmacistStockView.as_view(), name="pharmacistStock"),
    path('pharmacist_list/',pharmacistDetailsList.as_view(), name="pharmacist_list"),
    path('pharmacist_biding/',pharmacistBidingView.as_view(), name="pharmacist_biding"),
    path('win_loss_biding_count/',winLossBidingCount.as_view(), name="win_loss_biding_count"),
    path('pharmacist_ordar_tracking/',pharmacistOrdarTracking.as_view(), name="pharmacist_ordar_tracking"),
    path('pharmacist_missed_ordar_tracking/',pharmacistMissedOrdarTracking.as_view(), name="pharmacist_ordar_tracking"),
]