# Project Summary & Technical Report

## Project Overview
**AI Algorithmic Trading Dashboard** (v3.0) is a comprehensive financial analysis tool designed to assist retail investors. It combines Artificial Intelligence (Deep Learning) with traditional technical and fundamental analysis to provide high-probability trading insights.

## Technology Stack

### 1. Frontend & UI
-   **Streamlit**: The core web framework used for rapid development.
-   **Plotly**: Interactive financial charting (Candlesticks, Volume, Indicators).
-   **Custom CSS**: Glassmorphism effects for the "Developer Badge".

### 2. Backend & Data Processing
-   **Python 3.8+**: Primary language.
-   **Pandas & NumPy**: Time-series manipulation and indicator calculations.
-   **YFinance**: Wrapper API for:
    -   Real-time Stock Data (OHLCV).
    -   Options Chains (Calls/Puts).
    -   Currency Exchange Rates (`USDINR=X`, `EURUSD=X`).

### 3. Artificial Intelligence (AI)
-   **TensorFlow & Keras**: Deep learning framework.
-   **Model Architecture**:
    -   **Bidirectional LSTM**: Captures temporal dependencies in both directions.
    -   **Dropout (0.2)**: Regularization to prevent overfitting.
    -   **Dense Layers**: Final regression output.
-   **Inference**: The `AIEngine` class encapsulates model loading, scaling, and prediction logic.

## Key Features & Logic

### 🧠 Smart Ticker Search
-   **Logic**: Uses a lookup dictionary (`SYMBOL_MAP`) and fuzzy string matching in `utils/market_data.py`.
-   **Benefit**: Users can type "Nvidia" or "Google" instead of remembering "NVDA" or "GOOG".

### 💱 Global Currency Converter
-   **Logic**: Fetches real-time exchange rates (e.g., USD to INR) using `yfinance`.
-   **Implementation**: A global multiplier is applied to all financial metrics (Price, Market Cap, Strike Prices, Predictions) before display.

### ⛓️ Options Chain Analysis
-   **Logic**: Retrieves real-time Option Chains for selected expiry dates.
-   **Visualization**: Displays Call/Put tables with Strike Price, Last Price, Volume, and IV.

### 📈 Technical Indicators
-   **RSI (Relative Strength Index)**: Detects Overbought (>70) or Oversold (<30) conditions.
-   **MACD**: Identifies trend reversals via Signal Line crossovers.
-   **Bollinger Bands**: Visualizes volatility and potential breakout zones.

## Project Architecture
-   `app.py`: Main UI Controller.
-   `utils/market_data.py`: Data fetching layer (Stocks, Options, Forex).
-   `utils/indicators.py`: Mathematical analysis layer.
-   `utils/visuals.py`: Presentation layer (Charts).
-   `utils/ai_engine.py`: ML Inference layer.
