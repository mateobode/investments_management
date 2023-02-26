from django.db.models import Sum
from django.dispatch import receiver
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.serializers.loan import LoanSerializer
from backend.models.loan import Loan
from backend.models.cashflow import Cashflow
from rest_framework import viewsets
from django.core.cache import cache
from django.db.models.signals import post_save


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filterset_fields = "__all__"

    @action(detail=False)
    def get_statistics(self, request):

        investment_statistics = cache.get('statistics')
        if investment_statistics is not None:
            return Response(investment_statistics)

        nr_of_loans = Loan.objects.all().count()

        total_invested_amount_sum = 0
        for loan in Loan.objects.all():
            amount = loan.invested_amount
            total_invested_amount_sum += amount

        current_invested_amount = 0
        for loan in Loan.objects.all():
            if not loan.is_closed:
                amount = loan.invested_amount
                current_invested_amount += amount

        total_repaid_amount = 0
        for loan in Loan.objects.all():
            repayment_amount = loan.cash_flows.filter(type="Repayment").aggregate(Sum("amount")).get('amount__sum') or 0
            total_repaid_amount += repayment_amount

        average_realized_irr = 0
        for loan in Loan.objects.all():
            if loan.is_closed:
                weight_realize_irr = loan.realized_irr * (loan.invested_amount/total_invested_amount_sum)
                average_realized_irr += weight_realize_irr

        investments_statistics = {
            'Number of loans': nr_of_loans,
            'Total invested amount': total_invested_amount_sum,
            'Current invested amount': current_invested_amount,
            'Total repaid amount': total_repaid_amount,
            'Average realized irr': average_realized_irr
        }

        cache.set('statistics', investment_statistics)

        return Response(investments_statistics)


@receiver(post_save, sender=Loan)
@receiver(post_save, sender=Cashflow)
def invalidate_statistics(sender, **kwargs):
    cache.delete('statistics')
