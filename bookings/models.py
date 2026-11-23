from datetime import timedelta

from django.db import models

from accounts.models import Car, User
from services.models import ServiceType


class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    ALLOWED_TRANSITIONS = {
        Status.PENDING: {Status.CONFIRMED, Status.CANCELLED},
        Status.CONFIRMED: {Status.IN_PROGRESS, Status.CANCELLED},
        Status.IN_PROGRESS: {Status.COMPLETED, Status.CANCELLED},
        Status.COMPLETED: set(),
        Status.CANCELLED: set(),
    }

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_requests")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="service_requests")
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, related_name="requests")
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    estimated_completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_date", "-scheduled_time"]

    def __str__(self):
        return f"{self.customer.email} - {self.service_type.name} on {self.scheduled_date}"

    def can_transition_to(self, new_status):
        return new_status in self.ALLOWED_TRANSITIONS.get(self.status, set())

    def save(self, *args, **kwargs):
        if not self.estimated_completion_date and self.scheduled_date:
            extra_days = 1 if self.service_type.estimated_duration_minutes > 240 else 0
            self.estimated_completion_date = self.scheduled_date + timedelta(days=extra_days)
        super().save(*args, **kwargs)
