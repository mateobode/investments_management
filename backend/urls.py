from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.views.cashflow import CashFlowViewSet
from backend.views.csv_upload import csv_upload
from backend.views.loan import LoanViewSet


router = DefaultRouter()
router.register(r'loans', LoanViewSet)
router.register(r'cashflows', CashFlowViewSet)

urlpatterns = [
    path("csv-upload/", csv_upload),
]

urlpatterns += router.urls
