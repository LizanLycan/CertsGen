from django.contrib import admin
from django.urls import path, include
from apps.api.views import (
    SignatureRegisterView
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(
    r"add/signature",
    SignatureRegisterView,
    base_name="register-signature"
)

urlpatterns = [
    path("", include(router.urls)),
]
