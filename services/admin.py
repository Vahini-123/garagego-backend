from django.contrib import admin

from .models import ServiceType


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "estimated_duration_minutes", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
