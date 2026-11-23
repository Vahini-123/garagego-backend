import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

STATUS_MESSAGES = {
    "CONFIRMED": "Your service request has been confirmed.",
    "IN_PROGRESS": "Your car is now being serviced.",
    "COMPLETED": "Your service has been completed. Your car is ready for pickup.",
    "CANCELLED": "Your service request has been cancelled.",
}


def send_status_update_email(booking):
    message = STATUS_MESSAGES.get(booking.status, f"Your service request status is now {booking.status}.")
    subject = f"Service Request Update - {booking.service_type.name}"
    body = (
        f"Hi,\n\n"
        f"{message}\n\n"
        f"Service: {booking.service_type.name}\n"
        f"Car: {booking.car.make} {booking.car.model} ({booking.car.registration_number})\n"
        f"Scheduled: {booking.scheduled_date} {booking.scheduled_time}\n"
        f"Estimated completion: {booking.estimated_completion_date or 'TBD'}\n\n"
        f"Thanks,\nGarageGo"
    )
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [booking.customer.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Status update email failed for booking %s", booking.pk)