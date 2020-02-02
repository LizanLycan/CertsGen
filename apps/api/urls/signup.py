from django.contrib import admin
from django.urls import path, include
from apps.api.views import (
    AccreditationAuthorityRegisterView,
    CertificationAuthorityRegisterView,
    CertifierRegisterView,
    RecipientRegisterView
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(
    r"register/accreditation-authority",
    AccreditationAuthorityRegisterView,
    base_name="register-accreditation-authority"
)
router.register(
    r"register/certification-authority",
    CertificationAuthorityRegisterView,
    base_name="register-certification-authority"
)
router.register(
    r"register/certifier",
    CertifierRegisterView,
    base_name="register-certifier-authority"
)
router.register(
    r"register/recipient",
    RecipientRegisterView,
    base_name="register-recipient-authority"
)

urlpatterns = [
    path("", include(router.urls)),
]
