
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

# Date selection input
prediction_option = st.selectbox("Select Prediction Option", ["Today", "Tomorrow", "One Week", "Custom Range"])

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

# Prediction date logic
if prediction_option == "Today":
    prediction_date = end
elif prediction_option == "Tomorrow":
    prediction_date = end + timedelta(days=1)
elif prediction_option == "One Week":
    prediction_date = end + timedelta(weeks=1)
elif prediction_option == "Custom Range":
    custom_start = st.date_input("Select Start Date")
    custom_end = st.date_input("Select End Date")
    prediction_dates = pd.date_range(start=custom_start, end=custom_end)

# Preprocess the data for model prediction
splitting_len = int(len(stock_data)*0.7)
x_test = pd.DataFrame(stock_data.Close[splitting_len:])

# Scale the data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(x_test[['Close']])

# Prepare input for the model
x_data = []
y_data = []
for i in range(100, len(scaled_data)):
    x_data.append(scaled_data[i-100:i])
    y_data.append(scaled_data[i])

x_data, y_data = np.array(x_data), np.array(y_data)

# Predict the stock price using the model
predictions = model.predict(x_data)

# Inverse transform the predictions
inv_pre = scaler.inverse_transform(predictions)
inv_y_test = scaler.inverse_transform(y_data)

# Create a DataFrame to store the results
ploting_data = pd.DataFrame(
    {'original_test_data': inv_y_test.reshape(-1),
     'predictions': inv_pre.reshape(-1)},
    index=stock_data.index[splitting_len+100:]
)

# Display the original and predicted values
st.subheader("Original values vs Predicted values")
st.write(ploting_data)

# Plot original vs predicted values
st.subheader('Original Close Price vs Predicted Close Price')
fig = plt.figure(figsize=(15,6))
plt.plot(pd.concat([stock_data.Close[:splitting_len+100], ploting_data], axis=0))
plt.legend(["Data- not used", "Original Test data", "Predicted Test data"])
st.pyplot(fig)

# Predict stock price for the selected prediction date
if prediction_option in ["Today", "Tomorrow", "One Week"]:
    st.write(f"Predicted price for {prediction_option}: {inv_pre[-1][0]}")
elif prediction_option == "Custom Range":
    st.subheader("Predicted Prices for Custom Date Range")
    for date in prediction_dates:
        st.write(f"Predicted price for {date}: {inv_pre[-1][0]}")
