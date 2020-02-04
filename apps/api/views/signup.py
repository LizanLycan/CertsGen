from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework import mixins, viewsets, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.api.helpers import contract_deployed
from apps.api.serializers import (
    SingUpAccreditationAuthoritySerializer,
    CertificationAuthoritySignUpSerializer,
    CertifierSignUpSerializer,
    RecipientSignUpSerializer
)
from apps.api.helpers import CustomAPIException, handling_errors
from apps.api.helpers.permission import (
    IsAccreditationAuthority,
    IsCertificationAuthority
)
from apps.authorities.models import (
    AccreditationAuthority,
    CertificationAuthority,
)
from apps.user_profile.models import (
    Certifier,
    Recipient
)
from apps.transactions.models import Transaction
from web3 import Web3
import json


class AccreditationAuthorityRegisterView(viewsets.GenericViewSet,
                                         mixins.CreateModelMixin,
                                         ):
    permission_classes = [AllowAny]
    serializer_class = SingUpAccreditationAuthoritySerializer

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

            accreditation = contract_deployed("AccreditationAuthorityManager")
            accreditation.functions.getAccreditationAuthorityCount().call()
            tx_hash = accreditation.functions.insertAccreditationAuthority(
                Web3.toChecksumAddress(validated_data["owner"]),
                Web3.toBytes(text=validated_data["name"]),
                validated_data["id"]
            ).transact({"from": validated_data["owner"]})
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

        user_created = User.objects.create(
            username=validated_data["email"].lower(),
            email=validated_data["email"].lower(),
            password=make_password(validated_data["password"].lower()),
            first_name=validated_data["name"],
            last_name="",
            is_active=True,
        )

        a_authority = AccreditationAuthority.objects.create(
            address=accreditation.functions.getAccreditationAuthority(
                Web3.toChecksumAddress(validated_data["owner"])
            ).call(),
            owner=validated_data["owner"],
            user=user_created
        )

        Transaction.objects.create(
            hash=tx_hash,
            type=Transaction.INSERT,
            content_object=a_authority
        )

        token, created = Token.objects.get_or_create(user=user_created)

        return Response({"token": token.key})


class CertificationAuthorityRegisterView(viewsets.GenericViewSet,
                                         mixins.CreateModelMixin,
                                         ):
    permission_classes = [IsAccreditationAuthority]
    serializer_class = CertificationAuthoritySignUpSerializer

    def create(self, request, *args, **kwargs):
        """
        Defines de POST method for register CertificationAuthority

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
            aa = AccreditationAuthority.objects.get(user=request.user)
            aa_instance = contract_deployed("AccreditationAuthority", address=aa.address)
            cert_manager_address = aa_instance.functions.getCertificationManager().call()
            cert_manager = contract_deployed("CertificationAuthorityManager", address=cert_manager_address)
            tx_hash = cert_manager.functions.insertCertificationAuthority(
                aa.address,
                Web3.toChecksumAddress(validated_data["owner"]),
                Web3.toBytes(text=validated_data["name"]),
                validated_data["id"]
            ).transact({"from": validated_data["owner"]})
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

        user_created = User.objects.create(
            username=validated_data["email"].lower(),
            email=validated_data["email"].lower(),
            first_name=validated_data["name"],
            last_name="",
            is_active=True,
        )

        c_authority = CertificationAuthority.objects.create(
            address=cert_manager.functions.getCertificationAuthority(
                Web3.toChecksumAddress(validated_data["owner"])
            ).call(),
            owner=validated_data["owner"],
            user=user_created
        )

        Transaction.objects.create(
            hash=tx_hash,
            type=Transaction.INSERT,
            content_object=c_authority
        )

        token, created = Token.objects.get_or_create(user=user_created)

        return Response({"token": token.key})


class CertifierRegisterView(viewsets.GenericViewSet,
                            mixins.CreateModelMixin,
                            ):
    permission_classes = [IsCertificationAuthority]
    serializer_class = CertifierSignUpSerializer

    def create(self, request, *args, **kwargs):
        """
        Defines de POST method for register Certifier

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
            ca = CertificationAuthority.objects.get(user=request.user)
            ca_instance = contract_deployed("CertificationAuthority", address=ca.address)
            certifier_manager_address = ca_instance.functions.getCertifierManager().call()
            cert_manager = contract_deployed("CertifierManager",
                                             address=certifier_manager_address
                                             )
            tx_hash = cert_manager.functions.insertCertifier(
                ca.address,
                Web3.toChecksumAddress(validated_data["owner"]),
                Web3.toBytes(text=validated_data["name"]),
                Web3.toBytes(text=validated_data["email"]),
                Web3.toBytes(text=validated_data["id"]),
                validated_data["id_number"]
            ).transact({"from": validated_data["owner"]})
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

        user_created = User.objects.create(
            username=validated_data["email"].lower(),
            email=validated_data["email"].lower(),
            first_name=validated_data["name"],
            last_name="",
            is_active=True,
        )

        certifier = Certifier.objects.create(
            address=cert_manager.functions.getCertifier(
                Web3.toChecksumAddress(validated_data["owner"])
            ).call(),
            owner=validated_data["owner"],
            user=user_created
        )

        Transaction.objects.create(
            hash=tx_hash,
            type=Transaction.INSERT,
            content_object=certifier
        )

        token, created = Token.objects.get_or_create(user=user_created)

        return Response({"token": token.key})


class RecipientRegisterView(viewsets.GenericViewSet,
                            mixins.CreateModelMixin,
                            ):
    permission_classes = [IsCertificationAuthority]
    serializer_class = RecipientSignUpSerializer

    def create(self, request, *args, **kwargs):
        """
        Defines de POST method for register Recipient

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
            ca = CertificationAuthority.objects.get(user=request.user)
            ca_instance = contract_deployed("CertificationAuthority", address=ca.address)
            recipient_manager_address = ca_instance.functions.getRecipientManager().call()
            recipient_manager = contract_deployed("RecipientManager",
                                                  address=recipient_manager_address
                                                  )
            tx_hash = recipient_manager.functions.insertRecipient(
                ca.address,
                Web3.toChecksumAddress(validated_data["owner"]),
                Web3.toBytes(text=validated_data["name"]),
                Web3.toBytes(text=validated_data["email"]),
                Web3.toBytes(text=validated_data["id"]),
                validated_data["id_number"]
            ).transact({"from": validated_data["owner"]})
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

        user_created = User.objects.create(
            username=validated_data["email"].lower(),
            email=validated_data["email"].lower(),
            first_name=validated_data["name"],
            last_name="",
            is_active=True,
        )

        recipient = Recipient.objects.create(
            address=recipient_manager.functions.getRecipient(
                Web3.toChecksumAddress(validated_data["owner"])
            ).call(),
            owner=validated_data["owner"],
            user=user_created
        )

        Transaction.objects.create(
            hash=tx_hash,
            type=Transaction.INSERT,
            content_object=recipient
        )

        token, created = Token.objects.get_or_create(user=user_created)

        return Response({"token": token.key})
