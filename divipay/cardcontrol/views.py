from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .tasks import *

# Create your views here.


class CardControlDetailView(APIView):

    def delete(self, request, pk, format=None):
        card_control = get_object_or_404(CardControlDetail, pk=pk)
        if card_control.delete():
            message = {"status" : "success"}
            return Response(message, status=status.HTTP_200_OK)


class CardControlListView(APIView):

    def get(self, request):
        card_controls = CardControlDetail.objects.all()
        serializer = CardControlSerializer(card_controls, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CardControlSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateTransactionListView(APIView):

    def post(self, request, format=None):

        result = get_transaction.delay(request.data['cc_id'])
        message = {"message": "Transaction Recorded"}
        return Response(message, status=status.HTTP_200_OK)


class CardDetailView(APIView):

    def post(self, request, format=None):
        result = post_card.delay()
        message = {"message": "Saved Card to DB"}
        return Response(message, status=status.HTTP_200_OK)
