from django.db import models
import uuid

# Create your models here.


# Create your models here.
class CardDetail(models.Model):
    # Assumptions:
    # balance - can have a max balance of 9,999,999,999
    # user_id - can have a max users of 9,999,999,999

    card_id = models.UUIDField(default=uuid.uuid4, editable=True, primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user_id = models.CharField(max_length=10,blank=False, default='')
    created_time = models.DateTimeField(auto_created=True)
    updated_time = models.DateTimeField(auto_now=False)


class TransactionDetail(models.Model):
    trans_id = models.UUIDField(default=uuid.uuid4, editable=True, primary_key=True)
    card_id = models.UUIDField(default=uuid.uuid4, editable=True)
    trans_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    merchant = models.CharField(max_length=64, default='')
    merchant_category = models.CharField(max_length=5, default='')
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)
    trans_error = models.BooleanField(default=True)
    trans_message = models.TextField(default="", blank=True)


class CardControlDetail(models.Model):
    cc_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    parent_card = models.ForeignKey(CardDetail, on_delete=models.CASCADE)
    category = models.TextField(default='', blank=True)
    merchant = models.TextField(default='', blank=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
