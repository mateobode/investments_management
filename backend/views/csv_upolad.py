from rest_framework.decorators import api_view
import pandas as pd

from backend.models.loan import Loan
from backend.models.cashflow import Cashflow
from backend.serializers.csv_upload import CSVUploadSerializer


@api_view(['post'])
def csv_upload(request):
    serializer = CSVUploadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    loans_df = pd.read_csv(request.FILES.get("loans"))
    cashflows_df = pd.read_csv(request.FILES.get("cashflows"))

    for _, loan_row in loans_df.iterrows():
        loan = Loan(identifier=loan_row["identifier"], issue_date=loan_row["issue_date"])
        cash_flows = cashflows_df[cashflows_df["loan_identifier"] == loan_row["identifier"]]
        for _, cash_flow_row in cash_flows.iterrows():
            cash_flow = Cashflow(loan_identifier=loan, reference_date=cash_flow_row["reference_date"], type=cash_flow_row["type"], amount=cash_flow_row["amount"])
            o=2


