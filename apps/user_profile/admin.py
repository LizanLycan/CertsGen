from django.contrib import admin
from .models import Certifier, Recipient


class CertifierAdmin(admin.ModelAdmin):
    pass


class RecipientAdmin(admin.ModelAdmin):
    pass


admin.site.register(Certifier, CertifierAdmin)
admin.site.register(Recipient, RecipientAdmin)
