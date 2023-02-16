from rest_framework import serializers
from backend.models.cashflow import Cashflow


class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashflow
        fields = "__all__"
