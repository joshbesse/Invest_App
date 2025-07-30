from invest.models import Price, Indicators
import yfinance as yf
import pandas as pd
import pandas_ta as ta

def fetch_price_data_batch(tickers, period="1mo", interval="1d"):
    # fetch price batch data from yfinance
    df = yf.download(tickers, period=period, interval=interval, group_by="ticker")

    return df

def split_batch_by_ticker(tickers, batch_data):
    # split batch price data based on ticker
    ticker_data = {}

    for ticker in tickers:
        ticker_df = batch_data[ticker].copy().reset_index()
        ticker_df["Ticker"] = ticker
        ticker_data[ticker] = ticker_df

    return ticker_data

def calculate_indicators(ticker_data):
    # calculate indicators for ticker data
    ticker_data["pct_return_1d"] = ticker_data["Close"].pct_change()
    ticker_data["sma_10"] = ta.sma(ticker_data["Close"], length=10)
    ticker_data["macd"] = ta.macd(ticker_data["Close"])["MACD_12_26_9"]
    ticker_data["macd_hist"] = ta.macd(ticker_data["Close"])["MACDh_12_26_9"]
    ticker_data["rsi_14"] = ta.rsi(ticker_data["Close"], length=14)
    ticker_data["roc_10"] = ta.roc(ticker_data["Close"], length=10)
    ticker_data["atr_14"] = ta.atr(high=ticker_data["High"], low=ticker_data["Low"], close=ticker_data["Close"], length=14)
    ticker_data["bollinger_bandwidth"] = ta.bbands(ticker_data["Close"], length=20)["BBBW_20_2.0"]
    ticker_data["obv"] = ta.obv(ticker_data["Close"], ticker_data["Volume"])
    ticker_data["volume_change_1d"] = ticker_data["Volume"].pct_change()

    return ticker_data

def store_price_and_indicators(complete_data):
    # store price data in Price and indicator data in Indicators    
    return 

split_batch_by_ticker(["AAPL", "GOOG"], fetch_price_data_batch(["AAPL", "GOOG"]))