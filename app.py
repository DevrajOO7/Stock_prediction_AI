import streamlit as st
import pandas as pd
from datetime import datetime
from utils import market_data, indicators, visuals, ai_engine

# Page Config
st.set_page_config(layout="wide", page_title="AI Trading Desk", page_icon="📈")

# Custom CSS for Glassmorphism Credit Badge
st.markdown("""
<style>
.fixed-badge {
    position: fixed;
    top: 50px;
    right: 20px;
    z-index: 999999;
    background: linear-gradient(135deg, #0077b5 0%, #00a0dc 100%); /* LinkedIn Blue Gradient */
    color: white;
    padding: 8px 12px;
    border-radius: 25px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 600;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
}
.fixed-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0,119,181,0.4);
}
.fixed-badge a {
    color: white !important;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
}
.linkedin-icon {
    width: 16px;
    height: 16px;
    fill: white;
}
</style>
<div class="fixed-badge">
    <a href="https://www.linkedin.com/in/devraj007/" target="_blank">
        <svg class="linkedin-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
        </svg>
        Developed by DEVRAJ
    </a>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Trading Control")

with st.sidebar.form("search_form"):
    user_input = st.text_input("Ticker or Company Name", "Nvidia")
    # Move other inputs inside the form so they don't trigger re-runs individually
    
    start_date = st.date_input("Start Date", datetime(datetime.now().year - 2, 1, 1))
    end_date = st.date_input("End Date", datetime.now())
    
    # Currency Converter
    currency = st.selectbox("Currency", ["USD", "INR", "EUR", "GBP", "CAD"])

    # Settings
    st.markdown("---")
    st.subheader("Settings")
    show_indicators = st.checkbox("Show Technical Indicators", True)
    enable_ai = st.checkbox("Enable AI Forecast", True)
    
    submitted = st.form_submit_button("Search 🔍")

if not submitted and "ticker" not in st.session_state:
    # First run default
    ticker = market_data.resolve_ticker("Nvidia")
    st.session_state["ticker"] = ticker
elif submitted:
    ticker = market_data.resolve_ticker(user_input)
    st.session_state["ticker"] = ticker
else:
    # Use previous state if just re-running for some other reason (though form prevents most)
    ticker = st.session_state.get("ticker", "NVDA")

# Re-fetch exchange rate based on selection (which is now in form state)
exchange_rate = market_data.get_exchange_rate(currency)

# Inputs moved to form above

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 12px; color: #888;">
        © 2024 AI Trading Desk.<br>All rights reserved.<br>
        <span style="font-style: italic;">Designed by DEVRAJ</span>
    </div>
    """, 
    unsafe_allow_html=True
)

# Fetch Basic Info for Header
stock_info = market_data.get_stock_info(ticker)
company_name = stock_info.get('longName', ticker)

# Robust Summary Fetching
summary = stock_info.get('longBusinessSummary')
if not summary:
    summary = stock_info.get('businessSummary')
if not summary:
    summary = stock_info.get('description')
if not summary:
    summary = "No detailed business summary available for this company."

# Main Dashboard
st.title(f"📈 {company_name} ({ticker})")

# Summary Expander
with st.expander("📝 Company Summary"):
    st.write(summary)

# 1. Real-Time Metrics
metrics = market_data.get_real_time_metrics(ticker)
if metrics:
    price = metrics['current_price'] * exchange_rate
    prev_close = metrics['previous_close'] * exchange_rate
    change = metrics['day_change_pct']
    
    col1, col2, col3 = st.columns(3)
    col1.metric(f"Current Price ({currency})", f"{price:,.2f}", f"{change:.2f}%")
    col2.metric(f"Previous Close ({currency})", f"{prev_close:,.2f}")
    col3.metric("Volume", f"{metrics['volume']:,}")
else:
    st.warning("Real-time data possibly delayed.")

# Fetch Data
with st.spinner(f"Fetching data for {ticker}..."):
    stock_df = market_data.get_stock_data(ticker, period="5y") # Fetch enough data
    
if not stock_df.empty:
    # Convert Data to Selected Currency
    if currency != "USD":
        stock_df[['Open', 'High', 'Low', 'Close']] = stock_df[['Open', 'High', 'Low', 'Close']] * exchange_rate
        
    stock_df = indicators.add_technical_indicators(stock_df)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Professional Chart", "🧠 AI Analysis", "⛓️ Options Chain", "🏢 Fundamentals"])
    
    with tab1:
        st.subheader("Price Action & Volume")
        # Update chart logic to accept currency symbol for axis if needed, or just rely on the converted df
        fig = visuals.create_stock_chart(stock_df, ticker, show_indicators)
        # Update Y-axis title dynamically
        fig.update_layout(yaxis_title=f"Price ({currency})")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.subheader("AI Prediction & Signals")
        col_ai_1, col_ai_2 = st.columns([2, 1])
        
        with col_ai_1:
            if enable_ai:
                ai = ai_engine.AIEngine()
                # Note: AI predicts based on original scaled data. 
                # We should probably predict first, then convert. 
                # Ideally, train on normalized data, predict normalized, inverse transform to USD, then convert to Target Currency.
                # Since our model logic is encapsulated:
                # 1. We pass original USD data (stock_df was converted above! Problem?)
                # Wait: stock_df is now in Target Currency. 
                # If model expects USD patterns, this scaling is fine (relative).
                # But the prediction will be in Target Currency units if input is Target Currency units? Yes, MinMax scaler handles the range.
                prediction = ai.predict_future(stock_df, days=1)
                
                if prediction is not None:
                    # Prediction is already in target currency because stock_df was converted
                    pred_value = prediction.iloc[0]['Predicted Price']
                    
                    pred_fig = visuals.create_prediction_chart(stock_df, prediction, ticker)
                    st.plotly_chart(pred_fig, use_container_width=True)
                    st.success(f"AI Predicted Next Close: {pred_value:,.2f} {currency}")
                else:
                    st.warning("AI Model not trained or data insufficient.")
        
        with col_ai_2:
            st.markdown("### Technical Signals")
            signals = indicators.check_signals(stock_df)
            for key, value in signals.items():
                st.info(f"**{key}**: {value}")
            
    with tab3:
        st.subheader("Options Chain Analysis")
        # Options logic
        # Default to nearest
        chain, dates = market_data.get_options_chain(ticker)
        if dates:
            selected_date = st.selectbox("Expiry Date", dates)
            chain, _ = market_data.get_options_chain(ticker, selected_date)
            
            st.write(" **Calls** (Betting Price Goes Up)")
            calls = chain.calls
            if not calls.empty:
                calls['lastPrice'] = calls['lastPrice'] * exchange_rate
                calls['strike'] = calls['strike'] * exchange_rate
                st.dataframe(calls[['strike', 'lastPrice', 'volume', 'impliedVolatility']].head(10))
            
            st.write(" **Puts** (Betting Price Goes Down)")
            puts = chain.puts
            if not puts.empty:
                puts['lastPrice'] = puts['lastPrice'] * exchange_rate
                puts['strike'] = puts['strike'] * exchange_rate
                st.dataframe(puts[['strike', 'lastPrice', 'volume', 'impliedVolatility']].head(10))
        else:
            st.info("No options data found for this ticker.")
            
    with tab4:
        st.subheader("Fundamental Data")
        info = market_data.get_stock_info(ticker)
        if info:
            st.json({
                "Sector": info.get('sector'),
                "Industry": info.get('industry'),
                "Market Cap": f"{info.get('marketCap', 0) * exchange_rate:,.0f} {currency}",
                "P/E Ratio": info.get('trailingPE'),
                "Forward P/E": info.get('forwardPE'),
                "52 Week High": f"{info.get('fiftyTwoWeekHigh', 0) * exchange_rate:,.2f} {currency}",
                "52 Week Low": f"{info.get('fiftyTwoWeekLow', 0) * exchange_rate:,.2f} {currency}"
            })
        else:
            st.warning("Fundamental data unavailable.")

else:
    st.error("No data found. Please check the ticker symbol.")
