from django.core.management.base import BaseCommand
from invest.utils.ticker_groups import get_today_ticker_group
from invest.utils.price import fetch_price_data_batch, split_batch_by_ticker, calculate_indicators, store_price_and_indicators
import logging
from pathlib import Path
from datetime import date

log_file = Path("invest/logs/price_pipeline.log")

logger = logging.getLogger("price_pipeline_logger")
logger.setLevel(logging.INFO)
logger.handlers.clear()

file_handler = logging.FileHandler(log_file, mode="a")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Collect and insert price data in Price table and calculate and insert indicators in Indicator table"

    def handle(self, *args, **options):
        logger.info(f"Date: {date.today()}")

        # get ticker group for that day
        try:
            tickers, group_index = get_today_ticker_group()
            logger.info(f"✅ Pipeline started - Group index: {group_index}")
        except Exception as e:
            logger.error(f"❌ Failed to get ticker group: {e}")
            return

        # fetch batch price data
        try:
            batch_data = fetch_price_data_batch(tickers)
            logger.info(f"✅ Fetched batch price data")
        except Exception as e:
            logger.error(f"❌ Failed to fetch batch price data: {e}")
            return

        # split batch into individual ticker data
        try:
            ticker_data = split_batch_by_ticker(tickers, batch_data)
            logger.info(f"✅ Split batch data")
        except Exception as e:
            logger.error(f"❌ Failed to split batch data: {e}")
            return
        
        success_count = 0
        failed = []

        missing = [ticker for ticker in tickers if ticker not in ticker_data]
        failed.extend(missing)

        # for each ticker data calculate indicators and store data
        for ticker, df in ticker_data.items():
            try:
                df = calculate_indicators(df)
                df = df.tail(5)
                store_price_and_indicators(ticker, df)
                success_count += 1
            except Exception as e:
                failed.append(ticker)
                logger.error(f"❌ {ticker} failed: {e}")
        
        logger.info(f"✅ Pipeline complete - {success_count} succeeded, {len(failed)} failed")
        if failed:
            logger.info(f"❌ Failed tickers: {failed}")