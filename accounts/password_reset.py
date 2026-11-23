import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()
logger = logging.getLogger(__name__)


class PasswordResetRequestView(APIView):
    """Sends a reset link. Always answers the same, so nobody can probe which emails exist."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = (request.data.get("email") or "").strip()
        if email:
            user = User.objects.filter(email__iexact=email, is_active=True).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
                try:
                    send_mail(
                        "Reset your password - GarageGo",
                        (
                            "Hi,\n\n"
                            "We received a request to reset your password. "
                            "Click the link below to choose a new one:\n\n"
                            f"{link}\n\n"
                            "This link expires in 1 hour. If you did not ask for this, "
                            "you can ignore this email.\n\n"
                            "GarageGo"
                        ),
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception:
                    logger.exception("Password reset email failed")
        return Response({"detail": "If that email is registered, a reset link has been sent."})


class PasswordResetConfirmView(APIView):
    """Checks the link's uid + token and saves the new password."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        uid = request.data.get("uid", "")
        token = request.data.get("token", "")
        password = request.data.get("password", "")

        try:
            user = User.objects.get(pk=urlsafe_base64_decode(uid).decode())
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, token):
            return Response({"detail": "This reset link is invalid or has expired."}, status=400)

        try:
            validate_password(password, user)
        except ValidationError as e:
            return Response({"detail": " ".join(e.messages)}, status=400)

        user.set_password(password)
        user.save()
        return Response({"detail": "Password updated. You can now sign in."})