
import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

# Title of the App
st.title("Stock Price Predictor App")

# Stock selection input
stock = st.text_input("Enter the Stock ID", "GOOG")

# Start and end date for stock data
end = datetime.now()
start = datetime(end.year-20, end.month, end.day)

# Fetch stock data
stock_data = yf.download(stock, start, end)

# Load the trained model
model = load_model("Latest_stock_price_model.keras")

# Display the fetched stock data
st.subheader("Stock Data")
st.write(stock_data)

# Define helper function to plot graph
def plot_graph(figsize, values, full_data, extra_data=0, extra_dataset=None):
    fig = plt.figure(figsize=figsize)
    plt.plot(values, 'Orange')
    plt.plot(full_data.Close, 'b')
    if extra_data:
        plt.plot(extra_dataset)
    return fig

# Display Moving Averages
for days in [250, 200, 100]:
    stock_data[f"MA_for_{days}_days"] = stock_data.Close.rolling(days).mean()
    st.subheader(f"Original Close Price and MA for {days} days")
    st.pyplot(plot_graph((15, 6), stock_data[f"MA_for_{days}_days"], stock_data, 0))

# Add custom date input for prediction range
st.subheader("Select Custom Prediction Date Range")
start_prediction = st.date_input("Start Prediction Date", end)
end_prediction = st.date_input("End Prediction Date", end + timedelta(days=7))

# Ensure end date is not earlier than start date
if end_prediction < start_prediction:
    st.error("End date must be after the start date.")

# Generate prediction range based on selected dates
days_between = (end_prediction - start_prediction).days + 1
prediction_range = [start_prediction + timedelta(days=i) for i in range(days_between)]

# Preprocess the data for model prediction
splitting_ratio = 0.8
train_size = int(splitting_ratio * len(stock_data))
train_data = stock_data[:train_size]
test_data = stock_data[train_size:]

# Placeholder: Perform predictions here (adjust as per your model's input requirements)
predictions = np.random.randn(len(prediction_range))  # Replace this with actual model prediction logic

# Plot prediction results
st.subheader(f"Predictions from {start_prediction} to {end_prediction}")
st.line_chart(predictions)

# Plot graph for the predicted range
st.pyplot(plot_graph((15, 6), predictions, stock_data, 0))

