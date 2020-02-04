from rest_framework import serializers
from apps.user_profile.models import Recipient, Certifier
from apps.certificate.models import Certificate
from apps.api.helpers import CustomAPIException
from web3 import Web3


class CertificateSerializer(serializers.Serializer):

    """
    This handles the validation process of all the data that comes in the
    request to create the required model instances for the Certificate
    """
    recipient_address = serializers.CharField(
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

    title = serializers.CharField(
        write_only=True,
        required=True,
        min_length=5,
        max_length=150,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 5",
            "max_length": "The password is too long > 150",
        },
    )

    description = serializers.CharField(
        write_only=True,
        required=True,
        min_length=5,
        max_length=250,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 5",
            "max_length": "The password is too long > 250",
        },
    )

    def validate(self, attrs):

        """
        This function validates the data that comes in hand from the request
        to validate it in the serialziers.
        :param attrs:  attributes passed to the serialaizer
        :return: attrs
        """
        if not Web3.isChecksumAddress(attrs["recipient_address"]):
            raise CustomAPIException(
                "Recipient is not a valid address.",
                1001
            )

        if not Recipient.objects.filter(
            address=attrs["recipient_address"]
        ).exists():
            raise CustomAPIException(
                "Recipient does not exist.",
                1003
            )

        if Certificate.objects.filter(
            title=attrs["title"]
        ).exists():
            raise CustomAPIException(
                "Certificate already registered.",
                1004
            )

        return attrs


class CertifierDependencySerializer(serializers.Serializer):

    """
    This handles the validation process of all the data that comes in the
    request to create the required model instances for the Certificate
    """
    certificate_address = serializers.CharField(
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

    from_owner = serializers.CharField(
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

    to_owner = serializers.CharField(
        write_only=True,
        required=True,
        min_length=5,
        max_length=150,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 5",
            "max_length": "The password is too long > 150",
        },
    )

    def validate(self, attrs):

        """
        This function validates the data that comes in hand from the request
        to validate it in the serialziers.
        :param attrs:  attributes passed to the serialaizer
        :return: attrs
        """
        if not Web3.isChecksumAddress(attrs["from_owner"]):
            raise CustomAPIException(
                "From is not a valid owner.",
                1001
            )

        if not Web3.isChecksumAddress(attrs["to_owner"]):
            raise CustomAPIException(
                "To is not a valid owner.",
                1001
            )

        if not Certifier.objects.filter(
            owner=attrs["from_owner"]
        ).exists():
            raise CustomAPIException(
                "From does not exist.",
                1004
            )

        if not Certifier.objects.filter(
            owner=attrs["to_owner"]
        ).exists():
            raise CustomAPIException(
                "To does not exist.",
                1004
            )

        if not Certificate.objects.filter(
            address=attrs["certificate_address"]
        ).exists():
            raise CustomAPIException(
                "Certificate does not exist.",
                1004
            )

        return attrs
