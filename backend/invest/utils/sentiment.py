import os
from dotenv import load_dotenv
import datetime
import requests
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

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

def analyze_sentiment(news_data):
    # perform sentiment analysis using FinBert on article title + description
    model_name = "yiyanghkust/finbert-tone"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()

    for _, texts in news_data.items():
        for text in texts:
            combined = f"{text['title']} {text['description']}"
            inputs = tokenizer(combined, return_tensors="pt")

            with torch.no_grad():
                outputs = model(**inputs)
                probs = F.softmax(outputs.logits, dim=1)
            
            sentiment_id = torch.argmax(probs, dim=1).item()
            label = model.config.id2label[sentiment_id]
            score = probs[0][sentiment_id].item()

            text["sentiment_score"] = score
            text["sentiment_label"] = label

data = fetch_news_data(["AOS",])