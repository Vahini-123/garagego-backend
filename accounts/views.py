from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car, User
from .permissions import IsAdminRole
from .serializers import CarSerializer, LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """Public signup - always creates a CUSTOMER account."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Public login - returns JWT access/refresh tokens plus the user profile."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(
            {
                "access": data["access"],
                "refresh": data["refresh"],
                "user": UserSerializer(data["user"]).data,
            }
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """The logged-in user's own profile (customer or admin)."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CarViewSet(viewsets.ModelViewSet):
    """
    Customers manage their own cars.
    Admins can see every car (read-only via the customer-management endpoints below).
    """

    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AdminCustomerListView(generics.ListAPIView):
    """Admin-only: list all customers (with their cars) for the admin panel."""

    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    queryset = User.objects.filter(role=User.Role.CUSTOMER).order_by("-date_joined")


class AdminCustomerDetailView(generics.RetrieveAPIView):
    """Admin-only: view a single customer's profile + cars."""

    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    queryset = User.objects.filter(role=User.Role.CUSTOMER)
