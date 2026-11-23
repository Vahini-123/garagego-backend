from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .password_reset import PasswordResetConfirmView, PasswordResetRequestView

from .views import (
    AdminCustomerDetailView,
    AdminCustomerListView,
    CarViewSet,
    LoginView,
    ProfileView,
    RegisterView,
)

router = DefaultRouter()
router.register("cars", CarViewSet, basename="car")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("admin/customers/", AdminCustomerListView.as_view(), name="admin-customer-list"),
    path("admin/customers/<int:pk>/", AdminCustomerDetailView.as_view(), name="admin-customer-detail"),
    path("", include(router.urls)),
    path("password-reset/", PasswordResetRequestView.as_view()),
path("password-reset/confirm/", PasswordResetConfirmView.as_view()),
]
