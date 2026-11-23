from django.db import models


class ServiceType(models.Model):
    """Admin-managed catalog entry, e.g. 'Oil Change', 'Wheel Alignment'."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration_minutes = models.PositiveIntegerField(default=60)
    estimated_completion_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
