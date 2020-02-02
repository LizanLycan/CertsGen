from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers, status
from apps.user_profile.models import (
    Certifier,
    Recipient
)
from apps.authorities.models import (
    CertificationAuthority,
    AccreditationAuthority
)
from apps.api.helpers import CustomAPIException
from web3 import Web3


class SingUpAccreditationAuthoritySerializer(serializers.Serializer):

    """
    This handles the validation process of all the data that comes in the
    request to create the required model instances for the 1st SingUp
    """
    owner = serializers.CharField(
        write_only=True,
        required=True,
        min_length=32,
        max_length=64,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 32",
            "max_length": "The password is too long > 64",
        },
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=52,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 8",
            "max_length": "The password is too long > 52",
        },
    )

    email = serializers.EmailField(
        required=True,
        write_only=True
    )

    name = serializers.CharField(
        required=True,
        write_only=True,
        min_length=2,
        max_length=150,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The first_name is too short < 2",
            "max_length": "The first_name is too long > 150",
        },
    )

    id = serializers.IntegerField(
        required=True,
        write_only=True,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
        },
    )

    def validate(self, attrs):

        """
        This function validates the data that comes in hand from the request
        to validate it in the serialziers.
        :param attrs:  attributes passed to the serialaizer
        :return: attrs
        """
        if not Web3.isChecksumAddress(attrs["owner"]):
            raise CustomAPIException(
                "Owner is not a valid address.",
                1001
            )

        if User.objects.filter(
            first_name__iexact=attrs["name"]
        ).exists():
            raise CustomAPIException(
                "Name Already in use.",
                1002
            )

        if User.objects.filter(
            email__iexact=attrs["email"]
        ).exists():
            raise CustomAPIException(
                "Email Already in use.",
                1002
            )

        if AccreditationAuthority.objects.filter(
            owner=attrs["owner"]
        ).exists():
            raise CustomAPIException(
                "Owner already register.",
                1003
            )

        return attrs


class CertificationAuthoritySignUpSerializer(serializers.Serializer):

    """
    This handles the validation process of all the data that comes in the
    request to create the required model instances for the 1st SingUp
    """
    owner = serializers.CharField(
        write_only=True,
        required=True,
        min_length=32,
        max_length=64,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 32",
            "max_length": "The password is too long > 64",
        },
    )

    email = serializers.EmailField(
        required=True,
        write_only=True
    )

    name = serializers.CharField(
        required=True,
        write_only=True,
        min_length=2,
        max_length=150,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The first_name is too short < 2",
            "max_length": "The first_name is too long > 150",
        },
    )

    id = serializers.IntegerField(
        required=True,
        write_only=True,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
        },
    )

    def validate(self, attrs):

        """
        This function validates the data that comes in hand from the request
        to validate it in the serialziers.
        :param attrs:  attributes passed to the serialaizer
        :return: attrs
        """
        if not Web3.isChecksumAddress(attrs["owner"]):
            raise CustomAPIException(
                "Owner is not a valid address.",
                1001
            )

        if User.objects.filter(
            first_name__iexact=attrs["name"]
        ).exists():
            raise CustomAPIException(
                "Name Already in use.",
                1002
            )

        if User.objects.filter(
            email__iexact=attrs["email"]
        ).exists():
            raise CustomAPIException(
                "Email Already in use.",
                1002
            )

        if CertificationAuthority.objects.filter(
            owner=attrs["owner"]
        ).exists():
            raise CustomAPIException(
                "Owner already register.",
                1003
            )

        return attrs


class CertifierSignUpSerializer(serializers.Serializer):

    """
    This handles the validation process of all the data that comes in the
    request to create the required model instances for the 1st SingUp
    """
    owner = serializers.CharField(
        write_only=True,
        required=True,
        min_length=32,
        max_length=64,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 32",
            "max_length": "The password is too long > 64",
        },
    )

    email = serializers.EmailField(
        required=True,
        write_only=True
    )

    name = serializers.CharField(
        required=True,
        write_only=True,
        min_length=2,
        max_length=150,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The first_name is too short < 2",
            "max_length": "The first_name is too long > 150",
        },
    )

    id = serializers.CharField(
        required=True,
        write_only=True,
        min_length=2,
        max_length=150,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The first_name is too short < 2",
            "max_length": "The first_name is too long > 150",
        },
    )

    id_number = serializers.IntegerField(
        required=True,
        write_only=True,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
        },
    )

    def validate(self, attrs):

        """
        This function validates the data that comes in hand from the request
        to validate it in the serialziers.
        :param attrs:  attributes passed to the serialaizer
        :return: attrs
        """
        if not Web3.isChecksumAddress(attrs["owner"]):
            raise CustomAPIException(
                "Owner is not a valid address.",
                1001
            )

        if User.objects.filter(
            first_name__iexact=attrs["name"]
        ).exists():
            raise CustomAPIException(
                "Name Already in use.",
                1002
            )

        if User.objects.filter(
            email__iexact=attrs["email"]
        ).exists():
            raise CustomAPIException(
                "Email Already in use.",
                1002
            )

        if Certifier.objects.filter(
            owner=attrs["owner"]
        ).exists():
            raise CustomAPIException(
                "Owner already register.",
                1003
            )

        return attrs


class RecipientSignUpSerializer(serializers.Serializer):

    """
    This handles the validation process of all the data that comes in the
    request to create the required model instances for the 1st SingUp
    """
    owner = serializers.CharField(
        write_only=True,
        required=True,
        min_length=32,
        max_length=64,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 32",
            "max_length": "The password is too long > 64",
        },
    )

    email = serializers.EmailField(
        required=True,
        write_only=True
    )

    name = serializers.CharField(
        required=True,
        write_only=True,
        min_length=2,
        max_length=150,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The first_name is too short < 2",
            "max_length": "The first_name is too long > 150",
        },
    )

    id = serializers.CharField(
        required=True,
        write_only=True,
        min_length=2,
        max_length=150,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The first_name is too short < 2",
            "max_length": "The first_name is too long > 150",
        },
    )

    id_number = serializers.IntegerField(
        required=True,
        write_only=True,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
        },
    )

    def validate(self, attrs):

        """
        This function validates the data that comes in hand from the request
        to validate it in the serialziers.
        :param attrs:  attributes passed to the serialaizer
        :return: attrs
        """
        if not Web3.isChecksumAddress(attrs["owner"]):
            raise CustomAPIException(
                "Owner is not a valid address.",
                1001
            )

        if User.objects.filter(
            first_name__iexact=attrs["name"]
        ).exists():
            raise CustomAPIException(
                "Name Already in use.",
                1002
            )

        if User.objects.filter(
            email__iexact=attrs["email"]
        ).exists():
            raise CustomAPIException(
                "Email Already in use.",
                1002
            )

        if Recipient.objects.filter(
            owner=attrs["owner"]
        ).exists():
            raise CustomAPIException(
                "Owner already register.",
                1003
            )

        return attrs
