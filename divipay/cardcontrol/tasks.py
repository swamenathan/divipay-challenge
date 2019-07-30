import requests

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .models import *
from celery.utils.log import get_task_logger

from celery import shared_task

from divipay.settings import *

# Get an instance of a logger
logger = get_task_logger(__name__)


@shared_task()
def get_transaction(cc_id_pk):

    headers = {'Authorization': 'Token ' + DIVIPAY_TOKEN}
    response = requests.get(DIVIPAY_API, headers=headers)

    trans_data = response.json()

    # logger.info('data = %s' % type(trans_data))

    try:
        cc_obj = get_object_or_404(CardControlDetail, pk=cc_id_pk)

        # Check if transaction belongs to the card
        # if trans_data['card'] != cc_obj.parent_card:
        #     return save_transaction(trans_data, True, 'Card doesnt match Transaction')

        # Check Category
        category = [item for item in cc_obj.category.split(',') if trans_data['merchant_category'] == item]

        if len(category) == 0:
            return save_transaction(trans_data, True, 'Incorrect Category')

        # Check Merchant
        logger.info('cc_obj merchant = %s' % cc_obj.merchant)
        merchant = [item for item in cc_obj.merchant.split(',') if trans_data['merchant'] == item]
        logger.info('merchant = %s' % trans_data['merchant'])
        logger.info('merchant list = %s ' % merchant)
        if len(merchant) == 0:
            return save_transaction(trans_data, True, 'Incorrect Merchant')

        # Check Max Value
        if trans_data['amount'] > cc_obj.max_value:
            return save_transaction(trans_data, True, 'Exceeded Max Control')

        # Check Min Value
        if trans_data['amount'] < cc_obj.min_value:
            return save_transaction(trans_data, True, 'Lower than Min Control')

        # Deduct parent card balance
        if cc_obj.parent_card.balance - trans_data['amount'] >= 0:
            # reduce balance
            parent_card = get_object_or_404(CardDetail, pk=cc_obj.parent_card.card_id)
            parent_card.balance = cc_obj.parent_card.balance - trans_data['amount']
            parent_card.save()
            return save_transaction(trans_data, False, 'Success')
        else:
            return save_transaction(trans_data, True, 'Insufficient balance')

    except ObjectDoesNotExist as e:
        logger.error("Unable to get Object.\n%s" % e)


def save_transaction(t_data, error_status, message):
    logger.info('message = %s ' % message)

    transaction = TransactionDetail.objects.create(
        trans_id=t_data['id'],
        card_id=t_data['card'],
        trans_amount=t_data['amount'],
        merchant=t_data['merchant'],
        merchant_category=t_data['merchant_category'],
        created_time=t_data['created'],
        updated_time=t_data['updated'],
        trans_error=error_status,
        trans_message=message)

    transaction.save()

    return


@shared_task()
def post_card():

    headers = {'Authorization': 'Token' + DIVIPAY_TOKEN}
    response = requests.post(DIVIPAY_API, headers=headers)

    trans_data = response.json()
    logger.info('trans_data = %s ' % trans_data)

    card = CardDetail.objects.create(
        card_id=trans_data['id'],
        balance=trans_data['balance'],
        user_id=trans_data['user'],
        created_time=trans_data['created'],
        updated_time=trans_data['updated'])

    card.save()