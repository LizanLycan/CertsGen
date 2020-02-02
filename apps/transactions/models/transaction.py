from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from model_utils.models import TimeStampedModel
from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('http://localhost:7545'))


class Transaction(TimeStampedModel):
    """
    Model for transaction.
    """
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    GET = "get"

    TYPES = (
        (INSERT, "Insert"),
        (UPDATE, "Update"),
        (DELETE, "Delete"),
        (GET, "Get"),
    )
    hash = models.BinaryField()
    type = models.CharField(
        max_length=25,
        choices=TYPES,
        default=GET
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        transaction = w3.eth.waitForTransactionReceipt(self.hash)
        return "({}) - {} => {}".format(transaction.transactionHash.hex(), self.type, self.content_type)
