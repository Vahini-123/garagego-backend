from django.contrib import admin

from .models import ServiceRequest


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "car", "service_type", "scheduled_date", "scheduled_time", "status"]
    list_filter = ["status", "service_type"]
    search_fields = ["customer__email", "car__registration_number"]
