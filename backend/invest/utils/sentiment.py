import os
from dotenv import load_dotenv
import datetime
import requests

load_dotenv()

def fetch_news_data(tickers, days_back=5):
    # fetch news articles and headlines from newsapi
    api_key = os.getenv("NEWSAPI_KEY")
    url = "https://newsapi.org/v2/everything"

    today = datetime.date.today()
    from_date = (today - datetime.timedelta(days_back)).strftime("%Y-%m-%d")

    for ticker in tickers:
        params = {
            "qInTitle": ticker,
            "q": f'"{ticker}" AND (stock OR earnings OR shares)',
            "from": from_date,
            "to": today,
            "sortBy": "relevancy",
            "language": "en",
            "pageSize": 100,
            "apiKey": api_key
        }

        response = requests.get(url, params=params).json()
        print(response)

fetch_news_data(["AAPL", ])