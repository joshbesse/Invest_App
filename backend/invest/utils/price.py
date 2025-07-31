from invest.models import Stock, Price, Indicators
import yfinance as yf
import pandas_ta as ta

def fetch_price_data_batch(tickers, period="3mo", interval="1d"):
    # fetch price batch data from yfinance
    df = yf.download(tickers, period=period, interval=interval, group_by="ticker", auto_adjust=False)

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
    ticker_data["pct_return_1d"] = ticker_data["Close"].pct_change(fill_method=None)
    ticker_data["sma_10"] = ta.sma(ticker_data["Close"], length=10)
    ticker_data["rsi_14"] = ta.rsi(ticker_data["Close"], length=14)
    ticker_data["roc_10"] = ta.roc(ticker_data["Close"], length=10)
    ticker_data["atr_14"] = ta.atr(high=ticker_data["High"], low=ticker_data["Low"], close=ticker_data["Close"], length=14)
    ticker_data["obv"] = ta.obv(ticker_data["Close"], ticker_data["Volume"])
    ticker_data["volume_change_1d"] = ticker_data["Volume"].pct_change(fill_method=None)

    macd_df = ta.macd(ticker_data["Close"])
    if macd_df is not None:
        ticker_data["macd"] = macd_df["MACD_12_26_9"]
        ticker_data["macd_hist"] = macd_df["MACDh_12_26_9"]

    bbands_df = ta.bbands(ticker_data["Close"], length=20)
    if bbands_df is not None:
        ticker_data["bollinger_bandwidth"] = bbands_df["BBB_20_2.0"]

    return ticker_data

def store_price_and_indicators(complete_data):
    # store price data in Price and indicator data in Indicators
    stock = Stock.objects.get(ticker=complete_data["Ticker"])

    for _, row in complete_data.iterrows():
        Price.objects.get_or_create(
            stock=stock,
            date=row["Date"],
            open_price=row["Open"],
            high_price=row["High"],
            low_price=row["Low"],
            close_price=row["Close"],
            volume=row["Volume"]
        )

        Indicators.objects.get_or_create(
            stock=stock,
            date=row["Date"],
            pct_return_1d=row["pct_return_1d"],
            sma_10=row["sma_10"],
            macd=row["macd"],
            macd_hist=row["macd_hist"],
            rsi_14=row["rsi_14"],
            roc_10=row["roc_10"],
            atr_14=row["atr_14"],
            bollinger_bandwidth=row["bollinger_bandwidth"],
            obv=row["obv"],
            volume_change_1d=row["volume_change_1d"]
        )