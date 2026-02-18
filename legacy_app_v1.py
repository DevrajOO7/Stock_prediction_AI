import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

st.title("Stock Price Predictor App")

# Input for stock symbol
stock = st.text_input("Enter the Stock ID", "GOOG")

# Date range selection
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(datetime.now().year - 20, 1, 1))
with col2:
    end_date = st.date_input("End Date", datetime.now())

# Refresh button
if st.button("Refresh Data"):
    st.cache_data.clear()

@st.cache_data
def load_data(stock, start, end):
    try:
        data = yf.download(stock, start, end)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except Exception as e:
        return None

data_load_state = st.text('Loading data...')
google_data = load_data(stock, start_date, end_date)
data_load_state.text('Loading data... done!')

if google_data is None or google_data.empty:
    st.error(f"Error loading data for {stock}. Please check the ticker symbol.")
else:
    st.subheader("Stock Data")
    st.write(google_data.tail())

    # Moving Averages
    def plot_ma(days):
        ma = google_data.Close.rolling(days).mean()
        return ma

    st.subheader('Moving Averages')
    ma_100 = google_data.Close.rolling(100).mean()
    ma_200 = google_data.Close.rolling(200).mean()
    
    # Interactive Chart for Moving Averages
    chart_data = pd.DataFrame({
        'Close': google_data['Close'],
        'MA100': ma_100,
        'MA200': ma_200
    }, index=google_data.index)
    st.line_chart(chart_data)

    # Prediction Logic
    @st.cache_resource
    def load_prediction_model():
        try:
            model = load_model("Latest_stock_price_model.keras")
            return model
        except:
            return None

    model = load_prediction_model()

    if model:
        # Prepare data for prediction
        splitting_len = int(len(google_data) * 0.7)
        if len(google_data) > 100:
            x_test = pd.DataFrame(google_data.Close[splitting_len:])
            
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(x_test[['Close']])

            x_data = []
            y_data = []

            for i in range(100, len(scaled_data)):
                x_data.append(scaled_data[i-100:i])
                y_data.append(scaled_data[i])

            x_data, y_data = np.array(x_data), np.array(y_data)

            predictions = model.predict(x_data)
            inv_pre = scaler.inverse_transform(predictions)
            inv_y_test = scaler.inverse_transform(y_data)

            ploting_data = pd.DataFrame(
                {
                    'Original Test Data': inv_y_test.reshape(-1),
                    'Predicted Test Data': inv_pre.reshape(-1)
                },
                index = google_data.index[splitting_len+100:]
            )

            st.subheader("Original values vs Predicted values")
            st.write(ploting_data.tail())

            st.subheader('Original Close Price vs Predicted Close Price')
            # Combine original data (for context) and predictions
            # Note: For chart alignment, it's easier to just plot the test segment comparison
            st.line_chart(ploting_data)
            
        else:
            st.warning("Not enough data to calculate predictions (need > 100 days).")
            
    else:
        st.error("Model file 'Latest_stock_price_model.keras' not found. Please train the model first.")