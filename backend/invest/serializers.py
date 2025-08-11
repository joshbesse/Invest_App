from rest_framework import serializers
from .models import Price, Indicators, Text, Sentiment

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["date", "open_price", "high_price", "low_price", "close_price", "volume"]

class IndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        fields = ["date", "pct_return_1d", "sma_10", "macd", "macd_hist", "rsi_14", "roc_10",
                  "atr_14", "bollinger_bandwidth", "obv", "volume_change_1d"]

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ["date", "source", "url", "title", "description", "sentiment_score", "sentiment_label"]

class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentiment
        fields = ["date", "num_texts", "sentiment_score"]