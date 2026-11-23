from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from accounts.models import Car
from services.models import ServiceType

from .models import ServiceRequest
from .emails import send_status_update_email


class ServiceRequestReadSerializer(serializers.ModelSerializer):
    customer_email = serializers.EmailField(source="customer.email", read_only=True)
    car_display = serializers.SerializerMethodField()
    service_name = serializers.CharField(source="service_type.name", read_only=True)

    class Meta:
        model = ServiceRequest
        fields = [
            "id", "customer", "customer_email", "car", "car_display",
            "service_type", "service_name", "scheduled_date", "scheduled_time",
            "estimated_completion_date", "status", "notes", "created_at", "updated_at",
        ]
        read_only_fields = fields

    def get_car_display(self, obj):
        return f"{obj.car.make} {obj.car.model} ({obj.car.registration_number})"


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ["id", "car", "service_type", "scheduled_date", "scheduled_time", "notes"]
        read_only_fields = ["id"]

    def validate_car(self, car):
        request = self.context["request"]
        if car.owner_id != request.user.id:
            raise serializers.ValidationError("You can only book a service for your own car.")
        return car

    def validate_service_type(self, service_type):
        if not service_type.is_active:
            raise serializers.ValidationError("This service is not currently offered.")
        return service_type

    def validate(self, attrs):
        scheduled_date = attrs.get("scheduled_date")
        scheduled_time = attrs.get("scheduled_time")

        if scheduled_date and scheduled_time:
            naive_dt = datetime.combine(scheduled_date, scheduled_time)
            scheduled_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())

            if scheduled_dt <= timezone.now():
                raise serializers.ValidationError(
                    {"scheduled_date": "Bookings must be scheduled for a future date and time."}
                )

        return attrs

    def create(self, validated_data):
        validated_data["customer"] = self.context["request"].user
        return super().create(validated_data)

class ServiceRequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ["status", "estimated_completion_date"]
        extra_kwargs = {"estimated_completion_date": {"required": False}}

    def validate_status(self, new_status):
        instance = self.instance
        if not instance.can_transition_to(new_status):
            raise serializers.ValidationError(
                f"Cannot move a request from '{instance.status}' to '{new_status}'."
            )
        return new_status

    def update(self, instance, validated_data):
        old_status = instance.status
        instance = super().update(instance, validated_data)
        if "status" in validated_data and instance.status != old_status:
            send_status_update_email(instance)
        return instance