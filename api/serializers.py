from rest_framework import serializers
from .models import VerificationRequest

class VerificationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRequest
        fields = "__all__"
        read_only_fields = ("status", "created_at", "updated_at")