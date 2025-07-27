from django.core.management.base import BaseCommand
from invest.models import Stock
import pandas as pd

class Command(BaseCommand):
    help = "Fill in stock table with tickers and names."

    def handle(self, *args, **options):
        # load S&P500 data from CSV file
        df = pd.read_csv("invest/data/SP500.csv")

        # iterate through each row in df
        for _, row in df.iterrows():
            # create row in Stock table
            Stock.objects.create(ticker=row["Symbol"], name=row["Name"])

        print("Stocks inserted.")