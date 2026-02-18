import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional, Dropout
from keras.callbacks import EarlyStopping

def download_data(stock_symbol):
    end = datetime.now()
    start = datetime(end.year - 20, end.month, end.day)
    data = yf.download(stock_symbol, start, end)
    return data

def preprocess_data(data):
    # Use only Close price
    close_data = data[['Close']]
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_data)
    
    x_data = []
    y_data = []
    
    # Create sequences of 100 days
    for i in range(100, len(scaled_data)):
        x_data.append(scaled_data[i-100:i])
        y_data.append(scaled_data[i])
        
    x_data, y_data = np.array(x_data), np.array(y_data)
    return x_data, y_data, scaler

def build_model(input_shape):
    model = Sequential()
    
    # Layer 1: Bidirectional LSTM with Dropout
    model.add(Bidirectional(LSTM(units=100, return_sequences=True), input_shape=input_shape))
    model.add(Dropout(0.2))
    
    # Layer 2: Bidirectional LSTM with Dropout
    model.add(Bidirectional(LSTM(units=80, return_sequences=False)))
    model.add(Dropout(0.2))
    
    # Dense Layers
    model.add(Dense(units=50, activation='relu'))
    model.add(Dense(units=25, activation='relu'))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_and_save_model(stock_symbol="GOOG"):
    print(f"Downloading data for {stock_symbol}...")
    data = download_data(stock_symbol)
    
    print("Preprocessing data...")
    x_data, y_data, scaler = preprocess_data(data)
    
    # Split into train and test
    splitting_len = int(len(x_data) * 0.7)
    x_train, y_train = x_data[:splitting_len], y_data[:splitting_len]
    x_test, y_test = x_data[splitting_len:], y_data[splitting_len:]
    
    print("Building model...")
    model = build_model((x_train.shape[1], 1))
    
    print("Training model...")
    # Add EarlyStopping
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    model.fit(x_train, y_train, 
              batch_size=32, 
              epochs=50,  # Increased epochs, early stopping will handle it
              validation_data=(x_test, y_test),
              callbacks=[early_stop])
    
    print("Saving model...")
    model.save("Latest_stock_price_model.keras")
    print("Model saved as 'Latest_stock_price_model.keras'")

if __name__ == "__main__":
    train_and_save_model()
