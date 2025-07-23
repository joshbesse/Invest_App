from rest_framework import serializers
from .models import Text, Price

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'stock', 'date', 'source', 'url', 'content', 'sentiment_score']

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'stock', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']