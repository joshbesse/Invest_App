import os
from dotenv import load_dotenv
import datetime
import requests
import pandas as pd
import torch
import torch.nn.functional as F
from invest.models import Stock, Text, Sentiment

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
            "q": f'"{ticker}" AND (stock OR earnings OR shares OR trading OR market)',
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

        news_data[ticker] = {}

        for article in response["articles"]:
            date = pd.to_datetime(article["publishedAt"]).strftime("%Y-%m-%d")
            if date not in news_data[ticker]:
                news_data[ticker][date] = []

            news_data[ticker][date].append({
                "date": date,
                "source": article["source"]["name"],
                "url": article["url"],
                "title": article["title"],
                "description": article["description"],
                "content": article["content"]
            })
        
    return news_data

def analyze_sentiment(text, tokenizer, model):
    # perform sentiment analysis using FinBert and store results
    combined = f"{text['title']} {text['description']}"
    inputs = tokenizer(combined, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
    
    sentiment_id = torch.argmax(probs, dim=1).item()
    label = model.config.id2label[sentiment_id]
    score = probs[0][sentiment_id].item()

    return score, label

def store_text(ticker, text, score, label):
    stock = Stock.objects.get(ticker=ticker)

    Text.objects.get_or_create(
        stock=stock,
        date=text["date"],
        source=text["source"],
        url=text["url"],
        title=text["title"],
        description=text["description"],
        content=text["content"],
        sentiment_score=score,
        sentiment_label=label
    )

def average_sentiment(scores):
    num_scores = len(scores)
    avg_sentiment = sum(scores) / num_scores

    return num_scores, avg_sentiment

def store_sentiment(ticker, date, num_texts, sentiment_score):
    stock = Stock.objects.get(ticker=ticker)

    Sentiment.objects.get_or_create(
        stock=stock,
        date=date,
        num_texts=num_texts,
        sentiment_score=sentiment_score
    )