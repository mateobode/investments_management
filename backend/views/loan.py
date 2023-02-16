from backend.serializers.loan import LoanSerializer
from backend.models.loan import Loan
from rest_framework import viewsets


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filterset_fields = "__all__"
