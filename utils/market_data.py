import yfinance as yf
import pandas as pd
from datetime import datetime


# Common Name to Ticker Mapping (Extend as needed)
SYMBOL_MAP = {
    "NVIDIA": "NVDA",
    "GOOGLE": "GOOG",
    "APPLE": "AAPL",
    "TESLA": "TSLA",
    "MICROSOFT": "MSFT",
    "AMAZON": "AMZN",
    "META": "META",
    "NETFLIX": "NFLX",
    "FACEBOOK": "META",
    "AMD": "AMD",
    "INTEL": "INTC"
}

def resolve_ticker(query):
    """
    Tries to resolve a user query (Name or Ticker) to a valid Ticker Symbol.
    """
    query = query.strip().upper()
    # Check if direct match in map
    if query in SYMBOL_MAP:
        return SYMBOL_MAP[query]
    
    # Check if any key contains the query (e.g. "NVIDIA CORP" -> "NVDA")
    # Simple fuzzy-ish match
    for name, ticker in SYMBOL_MAP.items():
        if query in name or name in query:
            return ticker
            
    # Default: Assume it's a ticker
    return query

def get_stock_data(ticker, period="2y", interval="1d"):
    """
    Fetches historical stock data.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        return df
    except Exception as e:
        return pd.DataFrame()

def get_stock_info(ticker):
    """
    Fetches fundamental data (P/E, Market Cap, Sector).
    """
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except:
        return {}

def get_options_chain(ticker, date=None):
    """
    Fetches options chain for a specific expiry date.
    If no date provided, uses the nearest expiry.
    """
    try:
        stock = yf.Ticker(ticker)
        dates = stock.options
        if not dates:
            return None, []
        
        target_date = date if date in dates else dates[0]
        opt = stock.option_chain(target_date)
        return opt, dates
    except Exception as e:
        return None, []

def get_exchange_rate(target_currency):
    """
    Fetches the exchange rate from USD to target_currency.
    Returns 1.0 if target is USD or if fetch fails.
    """
    if target_currency == "USD":
        return 1.0
    
    try:
        # Yahoo Finance symbols for currency are like 'EUR=X', 'INR=X'
        pair = f"{target_currency}=X"
        ticker = yf.Ticker(pair)
        # fast_info is reliable for currencies
        rate = ticker.fast_info.last_price
        return rate
    except:
        return 1.0

def get_real_time_metrics(ticker):
    """
    Simulates real-time metrics (Price, Change, Volume) 
    using the latest available fast data.
    """
    try:
        stock = yf.Ticker(ticker)
        fast_info = stock.fast_info
        return {
            "current_price": fast_info.last_price,
            "previous_close": fast_info.previous_close,
            "volume": fast_info.last_volume,
            "day_change_pct": ((fast_info.last_price - fast_info.previous_close) / fast_info.previous_close) * 100
        }
    except:
        # Fallback for some tickers
        return None
