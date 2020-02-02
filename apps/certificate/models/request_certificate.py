from django.db import models
from model_utils.models import TimeStampedModel
from apps.user_profile.models import Recipient, Certifier
from apps.authorities.models import CertificationAuthority


class RequestCertificate(TimeStampedModel):
    """
    Model for request certificate actions.
    """
    SIGNATURE = "signature"
    CREATION = "creation"

    TYPES = (
        (SIGNATURE, "Signature"),
        (CREATION, "Creation")
    )
    type = models.CharField(
        max_length=10,
        choices=TYPES
    )
    certification_authority = models.ForeignKey(CertificationAuthority, on_delete=models.PROTECT)
    recipient = models.ForeignKey(Recipient, on_delete=models.PROTECT)
    certifier = models.ForeignKey(Certifier, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return "Request: {}".format(self.certifier)
