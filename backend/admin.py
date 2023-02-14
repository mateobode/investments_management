from django.contrib import admin
from backend.models.loan import Loan
from backend.models.cashflow import Cashflow


admin.site.register(Loan)
admin.site.register(Cashflow)
