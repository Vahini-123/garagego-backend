from django.urls import path

from .views import (
    AdminServiceRequestListView,
    MyServiceRequestListView,
    ServiceRequestCreateView,
    ServiceRequestDetailView,
    ServiceRequestStatusUpdateView,
)

urlpatterns = [
    path("", ServiceRequestCreateView.as_view(), name="booking-create"),
    path("mine/", MyServiceRequestListView.as_view(), name="booking-mine"),
    path("<int:pk>/", ServiceRequestDetailView.as_view(), name="booking-detail"),
    path("<int:pk>/status/", ServiceRequestStatusUpdateView.as_view(), name="booking-status-update"),
    path("admin/all/", AdminServiceRequestListView.as_view(), name="booking-admin-list"),
]
