from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Cast
from xirr.math import xirr


class Loan(models.Model):
    identifier = models.CharField(max_length=10, unique=True)
    issue_date = models.DateField()
    total_amount = models.FloatField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    maturity_date = models.DateField()
    total_expected_interest_amount = models.FloatField()

    def __str__(self):
         return self.identifier

    @property
    def invested_amount(self):
        return abs(self.cash_flows.filter(type="funding").aggregate(Sum('amount')).get("amount__sum"))

    @property
    def investment_date(self):
        return self.cash_flows.filter(type="funding").annotate(
            investment_date=Cast(
                "reference_date",
                output_field=models.CharField()
            )
        ).values_list('investment_date', flat=True).get()

    @property
    def expected_interest_amount(self):
        return self.total_expected_interest_amount * (self.invested_amount / self.total_amount)

    @property
    def is_closed(self):
        if self.cash_flows.filter(type="repayment").aggregate(
                Sum("amount")
        ).get('amount__sum') >= (self.invested_amount + self.expected_interest_amount):
            return True
        else:
            return False

    @property
    def expected_irr(self):
        reference_date = self.cash_flows.filter(type="funding").values_list("reference_date").get()[0]
        funding_amount = self.cash_flows.filter(type="funding").values_list("amount").get()[0]
        maturity_date = self.maturity_date
        expected_repayment_amount = self.invested_amount + self.expected_interest_amount
        expected_irr = {reference_date: funding_amount, maturity_date: expected_repayment_amount}
        return xirr(expected_irr)

    @property
    def realized_irr(self):
        if self.is_closed:
            funding_reference_date = self.cash_flows.filter(type="funding").values_list("reference_date").get()[0]
            funding_amount = self.cash_flows.filter(type="funding").values_list("amount").get()[0]
            repayment_reference_date = self.cash_flows.filter(type="repayment").values_list("reference_date").get()[0]
            repayment_amount = self.cash_flows.filter(type="repayment").values_list("amount").get()[0]
            realized_irr = {funding_reference_date: funding_amount, repayment_reference_date: repayment_amount}
            return xirr(realized_irr)
