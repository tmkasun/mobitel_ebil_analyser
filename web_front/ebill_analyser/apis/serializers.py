from rest_framework import serializers
from home.models import Ebill


class EbillSerializer(serializers.Serializer):
    number = serializers.CharField(required=True)
    mobile_no = serializers.CharField(required=True)
    timestamp = serializers.CharField(required=True)
    account_no = serializers.CharField(required=False)
    units = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    cost = serializers.CharField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Ebill.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        return instance
