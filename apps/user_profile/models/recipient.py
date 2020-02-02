from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


class Recipient(TimeStampedModel):
    """
    Model for recipient profile.
    """
    address = models.CharField(max_length=128)
    owner = models.CharField(max_length=64)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
