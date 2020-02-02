from apps.api.helpers import CustomAPIException
from rest_framework import serializers
from apps.authorities.models import CertificationAuthority
from apps.user_profile.models import (
    Certifier,
    Recipient
)


class CertificationAuthorityTokenSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(
        queryset=CertificationAuthority.objects.all(),
        many=False,
        slug_field="user__username",
        write_only=True,
        required=True
    )

    class Meta:
        model = CertificationAuthority
        exclude = ('user', 'owner', 'address')


class CertifierTokenSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(
        queryset=Certifier.objects.all(),
        many=False,
        slug_field="user__username",
        write_only=True,
        required=True
    )

    class Meta:
        model = Certifier
        exclude = ('user', 'owner', 'address')


class RecipientTokenSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(
        queryset=Recipient.objects.all(),
        many=False,
        slug_field="user__username",
        write_only=True,
        required=True
    )

    class Meta:
        model = Recipient
        exclude = ('user', 'owner', 'address')
