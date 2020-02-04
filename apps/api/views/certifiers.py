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


class CertifiersView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                    ):
    permission_classes = [IsCertificationAuthority]

    def list(self, request, *args, **kwargs):
        try:
            ca = CertificationAuthority.objects.get(user=request.user)
            ca_instance = contract_deployed("CertificationAuthority", address=ca.address)

            certifiers_address = ca_instance.functions.getCertifierManager().call()
            certifiers_sc = contract_deployed("CertifierManager", address=certifiers_address)

            all_certifiers_sc = certifiers_sc.functions.getAllCertifiers().call()

            all_certifiers = list(map(
                lambda address:
                    contract_deployed(
                        "Certifier",
                        address=certifiers_sc.functions.getCertifier(address).call()
                    ).functions.getUser().call(),
                all_certifiers_sc
            ))
            print(all_certifiers)

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

        return Response([])
