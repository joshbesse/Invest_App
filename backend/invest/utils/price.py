import yfinance as yf

def fetch_price_data_batch(tickers, period="1mo", interval="1d"):
    # fetch price batch data from yfinance
    df = yf.download(tickers, period=period, interval=interval, group_by="ticker")

    return df