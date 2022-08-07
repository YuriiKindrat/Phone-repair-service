from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user.urls", namespace="user")),
    path("", include("repair_service.urls", namespace="repair_service")),
]
