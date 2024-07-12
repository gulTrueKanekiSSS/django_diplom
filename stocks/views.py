from rest_framework import viewsets

from stocks.models import Stocks
from stocks.serializers import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stocks.objects.all()
    serializer_class = StockSerializer
