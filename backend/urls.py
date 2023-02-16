from django.urls import path
from rest_framework.routers import DefaultRouter

from backend.views.cashflow import CashFlowViewSet
from backend.views.loan import LoanViewSet


router = DefaultRouter()
router.register(r'loans', LoanViewSet)
router.register(r'cashflows', CashFlowViewSet)

urlpatterns = [

]

urlpatterns += router.urls
