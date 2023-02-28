from celery import shared_task
from backend.models import Loan, Cashflow
from django.db.models import ObjectDoesNotExist


@shared_task
def csv_processing(loans, grouped_cashflows):
    for loan in loans:
        loan_identifier = loan.get("identifier")
        try:
            existing_loan = Loan.objects.get(identifier=loan_identifier)
            print(f"Loan {loan_identifier} already exists in the database.")
            continue
        except ObjectDoesNotExist:
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
            try:
                existing_cash_flow = Cashflow.objects.get(
                    loan_identifier=loan_identifier,
                    reference_date=cash_flow["reference_date"],
                    type=cash_flow["type"],
                )
                print(f"CashFlow for loan {loan_identifier} on {cash_flow['reference_date']} already exists!")
                continue
            except ObjectDoesNotExist:
                cash_flow = Cashflow(
                    loan=loan,
                    loan_identifier=loan.identifier,
                    reference_date=cash_flow["reference_date"],
                    type=cash_flow["type"],
                    amount=cash_flow["amount"]
                )
                cash_flow.save()
