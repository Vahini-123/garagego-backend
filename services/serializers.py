from rest_framework import serializers

from .models import ServiceType


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = [
            "id", "name", "description", "price",
            "estimated_duration_minutes", "is_active",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
