from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.TextField(unique=True, null=False, blank=False)
    name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.ticker

class Text(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    source = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=3, null=False, blank=False)

    def __str__(self):
        return f"{self.stock.ticker} - {self.date} - {self.sentiment_score}"

class Sentiment(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=3, null=False, blank=False)

    def __str__(self):
        return f"{self.stock.ticker} - {self.date} - {self.sentiment_score}"

class Price(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    open_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    high_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    low_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    close_price = models.DecimalField(max_digits=20, decimal_places=10, null=False, blank=False)
    volume = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.stock.ticker} - {self.date} - {self.close_price}"

class Prediction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    features_json = models.JSONField(null=True, blank=True)
    prediction = models.TextField(null=False, blank=False)
    actual_label = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.stock.ticker} - {self.date} - {self.prediction}"
    
class PriceChange(models.Model):
    TIMEFRAME_CHOICES = [
        ('day', 'Daily'),
        ('week', 'Weekly'),
        ('month', 'Monthly'),
    ]

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    timeframe = models.CharField(max_length=10, choices=TIMEFRAME_CHOICES, null=False, blank=False)
    start_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    end_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    change_pct = models.FloatField(null=False, blank=False)
    change_abs = models.DecimalField(max_digits=20, decimal_places=10, null=False, blank=False)

    def __str__(self):
        return f"{self.stock.ticker} - {self.timeframe} - Price Change: {self.change_pct:.2f}%"

class SentimentChange(models.Model):
    TIMEFRAME_CHOICES = [
        ('day', 'Daily'),
        ('week', 'Weekly'),
        ('month', 'Monthly'),
    ]

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    timeframe = models.CharField(max_length=10, choices=TIMEFRAME_CHOICES, null=False, blank=False)
    start_score = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    end_score = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    change_pct = models.FloatField(null=False, blank=False)
    change_abs = models.DecimalField(max_digits=5, decimal_places=3, null=False, blank=False)

    def __str__(self):
        return f"{self.stock.ticker} - {self.timeframe} - Sentiment Change: {self.change_pct:.2f}%"