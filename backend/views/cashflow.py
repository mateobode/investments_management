from backend.serializers.cashflow import CashFlowSerializer
from backend.models.cashflow import Cashflow
from rest_framework import viewsets


class CashFlowViewSet(viewsets.ModelViewSet):
    queryset = Cashflow.objects.all()
    serializer_class = CashFlowSerializer
    filterset_fields = "__all__"
