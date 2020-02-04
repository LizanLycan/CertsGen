from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework import mixins, viewsets, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.api.helpers import w3, contract_deployed, contract_to_deploy
from apps.api.serializers import (
    SignatureSerializer
)
from apps.api.helpers import CustomAPIException, handling_errors
from apps.api.helpers.permission import (
    IsCertifier,
    IsCertificationAuthority
)
from apps.authorities.models import (
    AccreditationAuthority,
    CertificationAuthority,
)
from apps.certificate.models import Certificate
from apps.user_profile.models import (
    Certifier,
    Recipient
)
from apps.transactions.models import Transaction
from web3 import Web3
import json


class SignatureRegisterView(viewsets.GenericViewSet,
                            mixins.CreateModelMixin,
                            ):
    permission_classes = [IsCertifier]
    serializer_class = SignatureSerializer

    def create(self, request, *args, **kwargs):
        """
        Defines de POST method for register AccreditationAuthority

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            if "error" in e.args[0]:
                raise e

            raise handling_errors(e.args[0].items())

        try:
            validated_data = serializer.validated_data
            certifier = Certifier.objects.get(user=request.user.id)
            certificate = contract_deployed("Certificate", address=validated_data["certificate_address"])

            """
            Catch all contracts involved 
            """
            certifiers_dependencies_address = certificate.functions.getCertifierDependencies().call()
            certifiers_dependencies_sc = contract_deployed(
                "CertifierDependencyManager",
                address=certifiers_dependencies_address
            )

            signatures_address = certificate.functions.getSignatures().call()
            signatures_sc = contract_deployed(
                "SignatureManager",
                address=signatures_address
            )

            """
            Make sign
            """
            nonce = w3.eth.getTransactionCount(certifier.owner)
            hash = w3.solidityKeccak(
                ['address', 'uint256', 'bytes'],
                [certifier.owner, nonce, Web3.toHex(text=validated_data["params"])]
            )
            sign = w3.eth.sign(certifier.owner, hexstr=hash.hex())

            signature_hash = signatures_sc.functions.insertSignature(
                certifier.owner,
                nonce,
                Web3.toHex(text=validated_data["params"]),
                sign
            ).transact({"from": certifier.owner})

            certifiers_dependencies_sc.functions.insertSignerNonce(
                certifier.owner,
                nonce
            ).transact({"from": certifier.owner})

        except ValueError as err:
            vm_error = json.loads(str(err).replace("\'", "\""))
            raise CustomAPIException(
                "{}".format(vm_error["message"]),
                1020
            )
        except Exception as err:
            raise CustomAPIException(
                "Undefined error, check connection to EVM: {}".format(str(err)),
                1021
            )

        certificate = Certificate.objects.get(
            address=validated_data["certificate_address"]
        )

        Transaction.objects.create(
            hash=signature_hash,
            type=Transaction.UPDATE,
            content_object=certificate
        )

        return Response({"detail": "OK"})
