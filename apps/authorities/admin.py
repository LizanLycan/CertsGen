from django.contrib import admin
from .models import CertificationAuthority, RequestCertificate, AccreditationAuthority


class CertificationAuthorityAdmin(admin.ModelAdmin):
    pass


class RequestCertificateAdmin(admin.ModelAdmin):
    pass


class AccreditationAuthorityAdmin(admin.ModelAdmin):
    pass


admin.site.register(CertificationAuthority, CertificationAuthorityAdmin)
admin.site.register(AccreditationAuthority, AccreditationAuthorityAdmin)
admin.site.register(RequestCertificate, RequestCertificateAdmin)
