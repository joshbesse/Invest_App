from rest_framework.views import APIView
from rest_framework.response import Response
from invest.models import Stock, Price, Indicators, Text, Sentiment
from invest.serializers import PriceSerializer, IndicatorsSerializer, TextSerializer, SentimentSerializer
from datetime import timedelta
from django.utils.timezone import now

# Create your views here.
class StockPageView(APIView):
    def get(self, request, ticker):
        ticker = ticker

        try:
            stock = Stock.objects.get(ticker=ticker.upper())
        except Stock.DoesNotExist:
            return Response({"detail": "Unknown ticker"}, status=404)
        
        price_qs = Price.objects.filter(stock=stock).order_by("-date")[:7]
        indicators_qs = Indicators.objects.filter(stock=stock).order_by("-date").first()
        text_qs = Text.objects.filter(stock=stock).order_by("-date")[:5]
        sentiment_qs = Sentiment.objects.filter(stock=stock).order_by("-date")[:7]

        return Response({
            "ticker": stock.ticker,
            "name": stock.name,
            "price": PriceSerializer(price_qs, many=True).data,
            "indicators": IndicatorsSerializer(indicators_qs).data,
            "texts": TextSerializer(text_qs, many=True).data,
            "sentiment": SentimentSerializer(sentiment_qs, many=True).data
        })