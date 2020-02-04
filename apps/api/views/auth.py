from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from apps.authorities.models import AccreditationAuthority, CertificationAuthority
from apps.user_profile.models import Certifier, Recipient
from apps.api.helpers import CustomAPIException
from apps.api.helpers.permission import (
    IsAccreditationAuthority,
    IsCertificationAuthority
)
from apps.api.serializers import (
    CertificationAuthorityTokenSerializer,
    CertifierTokenSerializer,
    RecipientTokenSerializer
)


class AccreditationAuthorityCustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        try:
            AccreditationAuthority.objects.get(user=user.id)
            # t = aa.transactions.first()
            # print(t.hash)
        except Exception:
            raise CustomAPIException("Accreditation Authority does not exist", 1100)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        })


class CertificationAuthorityCustomAuthToken(ObtainAuthToken):
    permission_classes = [IsAccreditationAuthority]
    serializer_class = CertificationAuthorityTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        cert_authority = serializer.validated_data['email']

        try:
            CertificationAuthority.objects.get(user=cert_authority.user.id)
        except Exception:
            raise CustomAPIException("Certification Authority does not exist", 1100)

        token, created = Token.objects.get_or_create(user=cert_authority.user)

        return Response({
            'token': token.key
        })


class CertifierCustomAuthToken(ObtainAuthToken):
    permission_classes = [IsCertificationAuthority]
    serializer_class = CertifierTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        certifier = serializer.validated_data['email']

        try:
            Certifier.objects.get(user=certifier.user.id)
        except Exception:
            raise CustomAPIException("Certifier does not exist", 1100)

        token, created = Token.objects.get_or_create(user=certifier.user)

        return Response({
            'token': token.key
        })


class RecipientCustomAuthToken(ObtainAuthToken):
    permission_classes = [IsCertificationAuthority]
    serializer_class = RecipientTokenSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        recipient = serializer.validated_data['email']

        try:
            Recipient.objects.get(user=recipient.user.id)
        except Exception:
            raise CustomAPIException("Recipient does not exist", 1100)

        token, created = Token.objects.get_or_create(user=recipient.user)

        return Response({
            'token': token.key
        })
