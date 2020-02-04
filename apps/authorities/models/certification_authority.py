from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.contenttypes.fields import GenericRelation
from apps.transactions.models import Transaction
from apps.user_profile.models import Certifier, Recipient


class CertificationAuthority(TimeStampedModel):
    """
    Model for certification authority profile.
    """
    address = models.CharField(max_length=128)
    owner = models.CharField(max_length=64)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    transactions = GenericRelation(Transaction)

    def __str__(self):
        return "{}".format(self.user.first_name)


class RequestCertificate(TimeStampedModel):
    """
    Model for requested certificates for certification authority
    """
    certification_authority = models.ForeignKey(CertificationAuthority, null=True, on_delete=models.PROTECT)
    certifier = models.ForeignKey(Certifier, null=True, blank=True, on_delete=models.PROTECT)
    recipient = models.ForeignKey(Recipient, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return "TO: {}, FROM {} {}".format(self.certification_authority, self.certifier, self.recipient)
