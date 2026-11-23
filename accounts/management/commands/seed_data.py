from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from services.models import ServiceType

STARTER_SERVICES = [
    {"name": "Oil Change", "description": "Standard engine oil and filter change.", "price": 999, "estimated_duration_minutes": 30},
    {"name": "Wheel Alignment", "description": "Four-wheel computerized alignment.", "price": 1499, "estimated_duration_minutes": 45},
    {"name": "Brake Inspection", "description": "Full brake pad, disc, and fluid check.", "price": 599, "estimated_duration_minutes": 30},
    {"name": "AC Service", "description": "AC gas top-up and filter cleaning.", "price": 1999, "estimated_duration_minutes": 60},
    {"name": "General Checkup", "description": "Multi-point vehicle health inspection.", "price": 499, "estimated_duration_minutes": 40},
]

DEFAULT_ADMIN_EMAIL = "admin@csms.local"
DEFAULT_ADMIN_PASSWORD = "ChangeMe123!"


class Command(BaseCommand):
    help = "Seeds the default admin account and starter service catalog."

    @transaction.atomic
    def handle(self, *args, **options):
        if not User.objects.filter(email=DEFAULT_ADMIN_EMAIL).exists():
            User.objects.create_superuser(
                email=DEFAULT_ADMIN_EMAIL,
                password=DEFAULT_ADMIN_PASSWORD,
                first_name="System",
                last_name="Admin",
            )
            self.stdout.write(self.style.SUCCESS(
                f"Created admin: {DEFAULT_ADMIN_EMAIL} / {DEFAULT_ADMIN_PASSWORD} (change this password!)"
            ))
        else:
            self.stdout.write("Admin already exists, skipping.")

        created = 0
        for entry in STARTER_SERVICES:
            _, was_created = ServiceType.objects.get_or_create(name=entry["name"], defaults=entry)
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new service(s) (of {len(STARTER_SERVICES)} total)."))
