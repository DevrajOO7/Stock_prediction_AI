import pandas as pd
import numpy as np

def add_technical_indicators(df):
    """
    Adds SMA, EMA, RSI, MACD, and Bollinger Bands to the DataFrame.
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Simple Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # Exponential Moving Averages
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    
    # RSI (Relative Strength Index)
    delta = df['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD (Moving Average Convergence Divergence)
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    df['BB_Std'] = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (2 * df['BB_Std'])
    df['BB_Lower'] = df['BB_Middle'] - (2 * df['BB_Std'])
    
    return df

def check_signals(df):
    """
    Generates Basic Buy/Sell signals based on latest data.
    Note: High Probability != Guaranteed.
    """
    if df.empty or len(df) < 200:
        return {}
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    signals = {
        'RSI_Status': 'Neutral',
        'Trend': 'Neutral',
        'MACD_Cross': 'None'
    }
    
    # RSI Logic
    if latest['RSI'] > 70:
        signals['RSI_Status'] = 'Overbought (Potential Sell)'
    elif latest['RSI'] < 30:
        signals['RSI_Status'] = 'Oversold (Potential Buy)'
        
    # Trend Logic (SMA Crossover)
    if latest['SMA_50'] > latest['SMA_200']:
        signals['Trend'] = 'Bullish (Golden Cross Area)'
    else:
        signals['Trend'] = 'Bearish'
        
    # MACD Logic
    if latest['MACD'] > latest['Signal_Line'] and prev['MACD'] <= prev['Signal_Line']:
        signals['MACD_Cross'] = 'Bullish Crossover'
    elif latest['MACD'] < latest['Signal_Line'] and prev['MACD'] >= prev['Signal_Line']:
        signals['MACD_Cross'] = 'Bearish Crossover'
        
    return signals
