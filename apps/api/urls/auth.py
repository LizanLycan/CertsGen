from django.contrib import admin
from django.urls import path, include
from apps.api.views import (
    AccreditationAuthorityCustomAuthToken,
    CertificationAuthorityCustomAuthToken,
    CertifierCustomAuthToken,
    RecipientCustomAuthToken
)

urlpatterns = [
    path(
        'auth/accreditation-authority/',
        AccreditationAuthorityCustomAuthToken.as_view()
    ),
    path(
        'auth/certification-authority/',
        CertificationAuthorityCustomAuthToken.as_view()
    ),
    path(
        'auth/certifier/',
        CertifierCustomAuthToken.as_view()
    ),
    path(
        'auth/recipient/',
        RecipientCustomAuthToken.as_view()
    ),
]
