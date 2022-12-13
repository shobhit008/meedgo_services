from django.urls import path, include
from .views import docUpdaload

urlpatterns = [
    path('doc_upload/',docUpdaload.as_view(), name="doc_upload"),
]