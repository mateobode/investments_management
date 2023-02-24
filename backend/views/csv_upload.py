from collections import defaultdict

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.tasks import csv_processing
from backend.serializers.csv_upload import CSVUploadSerializer
import pandas as pd
from itertools import groupby


@api_view(['post'])
def csv_upload(request):
    serializer = CSVUploadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    loans = request.FILES.get("loans")
    loans_df = pd.read_csv(loans)
    loans_dict = loans_df.to_dict(orient="records")

    cashflows = request.FILES.get("cashflows")
    cash_flows_df = pd.read_csv(cashflows)
    cash_flows_dict = cash_flows_df.to_dict(orient="records")
    grouped_cash_flows = defaultdict(list)
    for loan_identifier, loan_cashflows in groupby(cash_flows_dict, lambda x: x.get('loan_identifier')):
        grouped_cash_flows[loan_identifier].extend(list(loan_cashflows))

    csv_processing.delay(loans_dict, grouped_cash_flows)

    return Response("Files uploaded successfully!", status=status.HTTP_202_ACCEPTED)
