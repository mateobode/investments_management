from django.db import models

from backend.models.loan import Loan
from backend.utils import TYPES


class Cashflow(models.Model):
    loan = models.ForeignKey(Loan, related_name="cash_flows", on_delete=models.CASCADE)
    loan_identifier = models.CharField(max_length=15)
    reference_date = models.DateField()
    type = models.CharField(choices=TYPES, max_length=10)
    amount = models.FloatField()

    def __str__(self):
        return self.loan_identifier.identifier
