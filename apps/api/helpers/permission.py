from rest_framework import permissions
from apps.user_profile.models import Certifier, Recipient
from apps.authorities.models import AccreditationAuthority, CertificationAuthority

"""
Certifier permissions
"""


def is_certifier(user):

    try:
        Certifier.objects.get(
            user=user.id
        )
        return True
    except Exception:
        return False


class IsCertifier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and is_certifier(request.user)


"""
Recipient permissions
"""


def is_recipient(user):

    try:
        Recipient.objects.get(
            user=user.id
        )
        return True
    except Exception:
        return False


class IsRecipient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and is_recipient(request.user)


"""
Certification Authority Permissions
"""


def is_certification_authority(user):

    try:
        CertificationAuthority.objects.get(
            user=user.id
        )
        return True
    except Exception:
        return False


class IsCertificationAuthority(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and is_certification_authority(request.user)


"""
Accreditation Authority Permissions
"""


def is_accreditation_authority(user):

    try:
        AccreditationAuthority.objects.get(
            user=user.id
        )
        return True
    except Exception:
        return False


class IsAccreditationAuthority(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and is_accreditation_authority(request.user)
