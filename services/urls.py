from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActiveServiceListView, ServiceTypeViewSet

router = DefaultRouter()
router.register("", ServiceTypeViewSet, basename="service")

urlpatterns = [
    path("active/", ActiveServiceListView.as_view(), name="service-active-list"),
    path("", include(router.urls)),
]
