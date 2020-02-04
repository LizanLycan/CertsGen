from django.contrib import admin
from .models import Certificate


class CertificateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Certificate, CertificateAdmin)
