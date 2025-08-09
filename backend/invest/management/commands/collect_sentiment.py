from django.core.management.base import BaseCommand
from invest.utils.ticker_groups import get_today_ticker_group
from invest.utils.sentiment import fetch_news_data, analyze_sentiment, store_text, average_sentiment, store_sentiment
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
from pathlib import Path
from datetime import date

log_file = Path("invest/logs/sentiment_pipeline.log")

logger = logging.getLogger("sentiment_pipeline_logger")
logger.setLevel(logging.INFO)
logger.handlers.clear()

file_handler = logging.FileHandler(log_file, "a")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Collect, perform sentiment analysis, and insert text data in Text table and average sentiment in Sentiment table"

    def handle(self, *args, **options):
        logger.info(f"Date: {date.today()}")

        # get ticker group for that day
        try:
            tickers, group_index = get_today_ticker_group()
            logger.info(f"✅ Pipeline started - Group index: {group_index}")
        except Exception as e:
            logger.error(f"❌ Failed to get ticker group: {e}")
            return

        # fetch news data
        try:
            news_data = fetch_news_data(tickers)
            logger.info(f"✅ Fetched news data")
        except Exception as e:
            logger.error(f"❌ Failed to fetch news data: {e}")
            return

        # load FinBert tokenizer and model
        try:
            model_name = "yiyanghkust/finbert-tone"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            model.eval()
            logger.info(f"✅ Loaded FinBert tokenizer and model")
        except Exception as e:
            logger.error(f"❌ Failed to load FinBert tokenizer and model")
            return
        
        success_count = 0
        failed = []

        # for every text perform sentiment analysis, store in Text, and build average sentiment dict
        sentiment_per_day = {}
        for ticker, date_dict in news_data.items():
            sentiment_per_day[ticker] = {}

            for date, texts in date_dict.items():
                if date not in sentiment_per_day[ticker]:
                    sentiment_per_day[ticker][date] = []

                for text in texts:
                    try:
                        score, label = analyze_sentiment(text, tokenizer, model)
                        sentiment_per_day[ticker][date].append(score)
                        store_text(ticker, text, score, label)
                        success_count += 1
                    except Exception as e:
                        failed.append((ticker, text['title']))
                        logger.error(f"❌ {ticker} {text['title']} failed: {e}")
        
        logger.info(f"✅ Text storage complete - {success_count} texts stored, {len(failed)} failed")
        if failed:
            logger.error(f"❌ Failed texts: {failed}")

        success_count = 0
        failed = []

        # for every ticker and date calculate average sentiment score
        for ticker, date_scores in sentiment_per_day.items():
            for date, scores in date_scores.items():
                try:
                    num_texts, average_sentiment_score = average_sentiment(scores)
                    store_sentiment(ticker, date, num_texts, average_sentiment_score)
                    success_count += 1
                except Exception as e:
                    failed.append((ticker, date))
                    logger.error(f"❌ {ticker} {date} failed: {e}")
        
        logger.info(f"✅ Average sentiment storage complete - {success_count} dates stored, {len(failed)} failed")
        if failed:
            logger.error(f"❌ Failed dates: {failed}")