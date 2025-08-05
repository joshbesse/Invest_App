import os
from dotenv import load_dotenv
import datetime
import requests
import pandas as pd

load_dotenv()

def fetch_news_data(tickers, days_back=5):
    # fetch news articles and headlines from newsapi
    api_key = os.getenv("NEWSAPI_KEY")
    url = "https://newsapi.org/v2/everything"

    today = datetime.date.today()
    from_date = (today - datetime.timedelta(days_back)).strftime("%Y-%m-%d")

    news_data = {}

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

        if response["status"] != "ok":
            continue

        news_data[ticker] = []

        for article in response["articles"]:
            news_data[ticker].append({
                "date": pd.to_datetime(article["publishedAt"]).strftime("%Y-%m-%d"),
                "source": article["source"]["name"],
                "url": article["url"],
                "title": article["title"],
                "description": article["description"],
                "content": article["content"]
            })
        
    return news_data