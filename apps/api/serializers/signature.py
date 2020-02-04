from rest_framework import serializers
from apps.user_profile.models import Recipient, Certifier
from apps.certificate.models import Certificate
from apps.api.helpers import CustomAPIException
from web3 import Web3


class SignatureSerializer(serializers.Serializer):

    """
    This handles the validation process of all the data that comes in the
    request to create the required model instances for the Signatures
    """
    params = serializers.CharField(
        write_only=True,
        required=True,
        min_length=1,
        max_length=32,
        error_messages={
            "blank": "This Field can't be empty",
            "required": "This field is required",
            "min_length": "The password is too short < 1",
            "max_length": "The password is too long > 32",
        },
    )

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

    def validate(self, attrs):

        """
        This function validates the data that comes in hand from the request
        to validate it in the serialziers.
        :param attrs:  attributes passed to the serialaizer
        :return: attrs
        """
        if not Web3.isChecksumAddress(attrs["certificate_address"]):
            raise CustomAPIException(
                "Certificate is not a valid address.",
                1001
            )

        if not Certificate.objects.filter(
            address=attrs["certificate_address"]
        ).exists():
            raise CustomAPIException(
                "Certificate does not exist.",
                1004
            )

        return attrs
