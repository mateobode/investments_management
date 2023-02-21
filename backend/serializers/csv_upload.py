from rest_framework import serializers


class CSVUploadSerializer(serializers.Serializer):
    loans = serializers.FileField()
    cashflows = serializers.FileField()

    class Meta:
        fields = ["loans", "cashflows"]
