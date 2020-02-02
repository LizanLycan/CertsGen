from django.contrib import admin
from django.urls import path, include
from apps.api.views import (
    CertificateRegisterView,
    CertifierDependencyView,
    GetCertificateView
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(
    r"register/certificate",
    CertificateRegisterView,
    base_name="register-certificate"
)

router.register(
    r"add/certifier-dependency",
    CertifierDependencyView,
    base_name="add-certifier-dependency"
)

router.register(
    r"get/certificates",
    GetCertificateView,
    base_name="get-certificates"
)

urlpatterns = [
    path("", include(router.urls)),
]
