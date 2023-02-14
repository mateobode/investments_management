from django.db import models

from backend.models.loan import Loan
from backend.utils import TYPES


class Cashflow(models.Model):
    loan_identifier = models.ForeignKey(Loan, related_name="loans", on_delete=models.CASCADE)
    reference_date = models.DateField()
    type = models.CharField(choices=TYPES, max_length=10)
    amount = models.FloatField()

    def __str__(self):
        return self.loan_identifier.identifier
