from rest_framework import serializers
from backend.models.loan import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

    def save(self, **kwargs):
        instance = super(LoanSerializer, self).save()
        # instance.invested_amount
        # instance.investment_date
        # instance.expected_interest_amount
        # instance.is_closed
        # instance.expected_irr
        # instance.realized_irr
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["invested_amount"] = instance.invested_amount
        rep["investment_date"] = instance.investment_date
        rep["expected_interest_amount"] = instance.expected_interest_amount
        rep["is_closed"] = instance.is_closed
        rep["expected_irr"] = instance.expected_irr
        rep["realized_irr"] = instance.realized_irr
        return rep
