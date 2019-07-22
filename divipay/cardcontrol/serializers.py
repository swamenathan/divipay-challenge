from rest_framework import serializers
from .models import *


class CardControlSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardControlDetail
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionDetail
        fields = '__all__'

