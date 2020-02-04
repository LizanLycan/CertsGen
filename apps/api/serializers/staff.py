from rest_framework import serializers

from django.contrib.auth.models import User
from apps.user_profile.models import Certifier


class UserSerializer(serializers.ModelSerializer):

    """
    Custom Serializer for User
    """

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "username")


class StaffSerializer(serializers.ModelSerializer):

    """
    Custom serializer for Staff with User
    """

    user = UserSerializer()

    class Meta:

        model = Certifier
        fields = (
            # "id",
            "user",
            "is_admin",
            "ci",
            "type",
        )
