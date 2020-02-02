from django.urls import include, path

urlpatterns = [
    path("", include("apps.api.urls.auth")),
    path("", include("apps.api.urls.signup")),
    path("", include("apps.api.urls.certificate")),
    path("", include("apps.api.urls.signature")),
    path("", include("apps.api.urls.certifiers")),
]
