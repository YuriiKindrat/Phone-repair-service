from django.urls import path, include
from rest_framework import routers

from repair_service.views import RequestViewSet, InvoiceViewSet

router = routers.DefaultRouter()
router.register("requests", RequestViewSet),
router.register("invoice", InvoiceViewSet),


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "repair_service"
