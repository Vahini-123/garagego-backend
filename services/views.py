from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdminRole

from .models import ServiceType
from .serializers import ServiceTypeSerializer


class ServiceTypeViewSet(viewsets.ModelViewSet):
    """
    Full CRUD over the service catalog. Admin-only for write ops;
    read access is allowed for any authenticated user (so the customer
    UI can still show services in place, e.g. inside a booking's detail).
    """

    queryset = ServiceType.objects.all().order_by("name")
    serializer_class = ServiceTypeSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAdminRole()]


class ActiveServiceListView(generics.ListAPIView):
    """Customer-facing: only currently-active services, for the booking form."""

    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAuthenticated]
    queryset = ServiceType.objects.filter(is_active=True).order_by("name")
