from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
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
        return self.cash_flows.filter(type="Funding").aggregate(Sum('amount')).get("amount__sum")

    @property
    def investment_date(self):
        return self.cash_flows.filter(type="Funding").order_by("reference_date").first().reference_date

    @property
    def expected_interest_amount(self):
        return self.total_expected_interest_amount * (abs(self.invested_amount) / self.total_amount)

    @property
    def is_closed(self):
        repayments_sum = self.cash_flows.filter(type="Repayment").aggregate(Sum("amount")).get('amount__sum') or 0

        if repayments_sum >= (abs(self.invested_amount) + self.expected_interest_amount):
            return True
        else:
            return False

    @property
    def expected_irr(self):
        funding_amount = self.cash_flows.filter(type="Funding").values_list("amount").get()[0]
        expected_repayment_amount = abs(self.invested_amount) + self.expected_interest_amount
        expected_irr = {self.investment_date: funding_amount, self.maturity_date: expected_repayment_amount}
        return xirr(expected_irr)

    @property
    def realized_irr(self):
        # TODO: consult someone if this formula is correct
        if not self.is_closed:
            return 0

        first_repayment = self.cash_flows.filter(type="Repayment").first()

        if not first_repayment:
            return 0

        funding_amount = self.cash_flows.filter(type="Funding").values_list("amount").get()[0]
        realized_irr = {self.investment_date: funding_amount, first_repayment.reference_date: first_repayment.amount}
        return xirr(realized_irr)
