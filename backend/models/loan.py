from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


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
        return [loan.loans.values('amount') for loan in self.objects.filter(loans__type__exact="funding")]

    @property
    def investment_date(self):
        pass
        #return [loan.loans.values[] for loan in self.objects.filter(loans__reference_date=)]

    @property
    def expected_interest_amount(self):
        pass

    @property
    def is_closed(self):
        pass

    @property
    def expected_irr(self):
        pass

    @property
    def realized_irr(self):
        pass
