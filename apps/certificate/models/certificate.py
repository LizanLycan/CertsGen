from django.db import models
from model_utils.models import TimeStampedModel
from apps.transactions.models import Transaction
from apps.user_profile.models import Recipient, Certifier
from django.contrib.contenttypes.fields import GenericRelation


class Certificate(TimeStampedModel):
    """
    Model for certificate profile.
    """
    title = models.CharField(max_length=150, null=True)
    address = models.CharField(max_length=128)
    recipient = models.ForeignKey(Recipient, on_delete=models.PROTECT)
    certifiers = models.ManyToManyField(Certifier)
    transactions = GenericRelation(Transaction)

    def __str__(self):
        return "Certificate: {}".format(self.address)
