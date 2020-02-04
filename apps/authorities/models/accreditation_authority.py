from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.contenttypes.fields import GenericRelation
from apps.transactions.models import Transaction


class AccreditationAuthority(TimeStampedModel):
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
