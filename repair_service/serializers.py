from rest_framework import serializers

from repair_service.models import Request, Invoice


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ("phone_model", "problem_description")


class RequestListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ("id", "user", "phone_model", "problem_description", "status")


class MasterRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ("status",)


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = "__all__"
