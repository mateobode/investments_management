from rest_framework import serializers
from backend.models.loan import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["invested_amount"] = instance.invested_amount
        rep["investment_date"] = instance.investment_date
        rep["expected_interest_amount"] = instance.expected_interest_amount
        rep["is_closed"] = instance.is_closed
        rep["expected_irr"] = instance.expected_irr
        rep["realized_irr"] = instance.realized_irr
        return rep
