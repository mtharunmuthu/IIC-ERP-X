from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Login + IIC Dashboard
    path("admin/", admin.site.urls),

    # IIC ERP pages
    path("", include("iic.urls")),
]
