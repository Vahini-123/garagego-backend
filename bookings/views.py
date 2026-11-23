from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdminRole

from .models import ServiceRequest
from .serializers import (
    ServiceRequestCreateSerializer,
    ServiceRequestReadSerializer,
    ServiceRequestStatusUpdateSerializer,
)


class ServiceRequestCreateView(generics.CreateAPIView):
    """Customer creates a booking for one of their own cars."""

    serializer_class = ServiceRequestCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(ServiceRequestReadSerializer(obj).data, status=status.HTTP_201_CREATED)


class MyServiceRequestListView(generics.ListAPIView):
    """Customer's own bookings ('my requests')."""

    serializer_class = ServiceRequestReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ServiceRequest.objects.filter(customer=self.request.user).select_related(
            "car", "service_type", "customer"
        )


class AdminServiceRequestListView(generics.ListAPIView):
    """Admin's view of every booking, filterable by status/date/etc."""

    serializer_class = ServiceRequestReadSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "scheduled_date", "scheduled_time", "service_type"]
    queryset = ServiceRequest.objects.all().select_related("car", "service_type", "customer")


class ServiceRequestStatusUpdateView(generics.UpdateAPIView):
    """Admin (or the panel) transitions a booking's status; keeps both panels in sync."""

    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestStatusUpdateSerializer
    permission_classes = [IsAdminRole]
    http_method_names = ["patch"]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(ServiceRequestReadSerializer(obj).data)


class ServiceRequestDetailView(generics.RetrieveAPIView):
    """Owner (customer) or admin can view a single booking's detail."""

    serializer_class = ServiceRequestReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.is_superuser:
            return ServiceRequest.objects.all()
        return ServiceRequest.objects.filter(customer=user)