from django.core.paginator import Paginator, PageNotAnInteger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from transaction_location.models import Transaction
from transaction_location.serializers import TransactionSerializer


# Create your views here.
class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        transactions = Transaction.objects.all().order_by('name')

        paginator = Paginator(transactions, limit)
        try:
            transactions_page = paginator.page(page)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)

        serializer = TransactionSerializer(transactions_page, many=True)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TransactionPkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(instance=transaction)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(instance=transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)

        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
