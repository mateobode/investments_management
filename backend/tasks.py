import pandas as pd
from celery import shared_task
from backend.models import Loan, Cashflow


@shared_task
def csv_processing(loans, grouped_cashflows):
    for loan in loans:
        loan_identifier = loan.get("identifier")
        loan = Loan(
            identifier=loan_identifier,
            issue_date=loan.get("issue_date"),
            total_amount=loan.get("total_amount"),
            rating=loan.get("rating"),
            maturity_date=loan.get("maturity_date"),
            total_expected_interest_amount=loan.get("total_expected_interest_amount"),
        )
        loan.save()

        loan_cash_flows = grouped_cashflows.get(loan_identifier)

        for cash_flow in loan_cash_flows:
            cash_flow = Cashflow(
                loan=loan,
                loan_identifier=loan.identifier,
                reference_date=cash_flow["reference_date"],
                type=cash_flow["type"],
                amount=cash_flow["amount"]
            )
            cash_flow.save()
