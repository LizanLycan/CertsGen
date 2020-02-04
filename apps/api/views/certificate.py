from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework import mixins, viewsets, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.api.helpers import w3, contract_deployed, contract_to_deploy
from apps.api.serializers import (
    CertificateSerializer,
    CertifierDependencySerializer
)
from apps.api.helpers import CustomAPIException, handling_errors
from apps.api.helpers.permission import (
    IsCertifier,
    IsRecipient,
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


class CertificateRegisterView(viewsets.GenericViewSet,
                              mixins.CreateModelMixin,
                              ):
    permission_classes = [IsCertifier]
    serializer_class = CertificateSerializer

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

            recipient = Recipient.objects.get(address=validated_data["recipient_address"])
            certifier = Certifier.objects.get(user=request.user.id)
            recipient_sc = contract_deployed("Recipient", address=recipient.address)
            certifier_sc = contract_deployed("Certifier", address=certifier.address)
            certification_authority_sc = certifier_sc.functions.getCertificationAuthority().call()

            contract, tx_hash = contract_to_deploy(
                name="Certificate",
                from_address=certifier.owner,
                params=(
                    recipient_sc.address,
                    certifier_sc.address,
                    certification_authority_sc,
                    Web3.toBytes(text=validated_data["title"]),
                    Web3.toBytes(text=validated_data["description"]),
                )
            )
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

            certificate_manager_address = recipient_sc.functions.getCertificateManager().call()

            certificate_manager = contract_deployed(
                "CertificateManager",
                address=certificate_manager_address
            )
            certificate_manager.functions.insertCertificate(tx_receipt.contractAddress).transact(
                {"from": recipient.owner}
            )

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

        certificate = Certificate.objects.create(
            title=validated_data["title"],
            address=tx_receipt.contractAddress,
            recipient=recipient,
        )
        certificate.certifiers.add(certifier)

        Transaction.objects.create(
            hash=tx_hash,
            type=Transaction.INSERT,
            content_object=certificate
        )

        return Response({"certificate_address": tx_receipt.contractAddress})


class CertifierDependencyView(viewsets.GenericViewSet,
                              mixins.CreateModelMixin,
                              ):
    permission_classes = [IsCertificationAuthority]
    serializer_class = CertifierDependencySerializer

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
            ca = CertificationAuthority.objects.get(user=request.user.id)

            certifier_from = Certifier.objects.get(owner=validated_data["from_owner"])
            certifier_to = Certifier.objects.get(owner=validated_data["to_owner"])
            certificate = contract_deployed("Certificate", address=validated_data["certificate_address"])

            certifiers_dependencies_address = certificate.functions.getCertifierDependencies().call()
            certifiers_dependencies_sc = contract_deployed(
                "CertifierDependencyManager",
                address=certifiers_dependencies_address
            )
            tx_hash = certifiers_dependencies_sc.functions.insertCertifierDependency(
                validated_data["from_owner"],
                validated_data["to_owner"],
            ).transact({"from": ca.owner})

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
            hash=tx_hash,
            type=Transaction.UPDATE,
            content_object=certificate
        )

        return Response({"detail": "OK"})


class GetCertificateView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     ):
    permission_classes = [IsRecipient]

    def list(self, request, *args, **kwargs):
        try:
            recipient = Recipient.objects.get(user=request.user.id)

            recipient_sc = contract_deployed("Recipient", address=recipient.address)
            certificates = contract_deployed(
                "CertificateManager",
                address=recipient_sc.functions.getCertificateManager().call()
            ).functions.getAllCertificates().call()

            certificates_all = []
            for address in certificates:
                certificate = contract_deployed(
                    "Certificate",
                    address=address
                )
                info = certificate.functions.getInfo().call()
                dependencies = contract_deployed(
                    "CertifierDependencyManager",
                    address=certificate.functions.getCertifierDependencies().call()
                )
                certificates_all.append(
                    {
                        "title": Web3.toText(info[0]).rstrip('\x00'),
                        "info": Web3.toText(info[1]).rstrip('\x00'),
                        "address": address,
                        "is_validated": dependencies.functions.getCertifierDependencyCount().call() > 0
                    }
                )

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

        return Response(certificates_all)
