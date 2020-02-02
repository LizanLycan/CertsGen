from django.urls import path, include
from apps.api.views import (
    CertifiersView
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(
    r"get/certifiers",
    CertifiersView,
    base_name="get-certifiers"
)

urlpatterns = [
    path("", include(router.urls)),
]