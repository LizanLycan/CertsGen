from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel
from apps.transactions.models import Transaction
from django.contrib.contenttypes.fields import GenericRelation
# from apps.certificate.models import Certificate


class Certifier(TimeStampedModel):
    """
    Model for certifier profile.
    """

    address = models.CharField(max_length=128)
    owner = models.CharField(max_length=64)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    # certificates = models.ManyToManyField(Certificate, on_delete=models.PROTECT)
    transactions = GenericRelation(Transaction)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
