from django.core.management.base import BaseCommand
from invest.models import Stock
import logging
from pathlib import Path
import yfinance as yf
import time

log_file = Path("invest/logs/ticker_removal.log")

logger = logging.getLogger("ticker_removal_logger")
logger.setLevel(logging.INFO)
logger.handlers.clear()

file_handler = logging.FileHandler(log_file, mode="a")
formatter = logging.Formatter("[%(asctime)s] %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Remove incorrect/outdated tickers from Stock table"

    def handle(self, *args, **options):
        logger.info("Started cleaning Stock table")

        # retrieve all tickers from Stock
        tickers = list(Stock.objects.all())

        # check yfinance existance for each stock
        for ticker in tickers:
            try:
                df = yf.Ticker(ticker.ticker).history(period="1d")
                if df.empty:
                    ticker.delete()
                    logger.info(f"{ticker.ticker} Deleted")
            except Exception as e:
                ticker.delete()
                logger.info(f"{ticker.ticker} Deleted")
            
            time.sleep(1)
        
        logger.info("Cleaning completed")