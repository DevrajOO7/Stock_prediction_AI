# AI Algorithmic Trading Dashboard (Project 3.0)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stockpredai.streamlit.app/)

A professional-grade financial analysis tool powered by Deep Learning (LSTM) and real-time market data. Analyze stocks, view options chains, and leverage AI predictions to make high-probability trading decisions.

**Developed by**: [DEVRAJ](https://www.linkedin.com/in/devraj007/) 🚀

## 🌟 New Features
-   **Smart Search**: Type "Nvidia", "Google", "Tesla" instead of tickers.
-   **Sidebar Search Button**: Prevents app reload while typing for a smoother experience.
-   **Global Currency Converter**: View prices in **USD, INR, EUR, GBP, CAD** instantly.
-   **Interactive Charts**: Professional Plotly Candlestick charts with Volume & Bollinger Bands.
-   **AI Predictions**: Uses a Bidirectional LSTM model to forecast price trends.
-   **Options Chain**: Real-time Call/Put data for market sentiment analysis.
-   **Technical Signals**: Auto-detects RSI Overbought/Oversold and MACD Crossovers.

## 🚀 How to Run Locally

### Prerequisites
1.  **Python 3.8+** installed.
2.  **Git** installed.

### Installation
1.  **Clone the Repository** (or download files):
    ```bash
    git clone https://github.com/yourusername/stock-predictionpro.git
    cd stock-predictionpro
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
-   **Run the App**:
    -   Double-click `run_app.bat` (Windows).
    -   Or run: `streamlit run app.py`

## 📤 How to Push to GitHub

If you want to host this code on your own GitHub:

1.  **Initialize Git**:
    Open your terminal/command prompt in the project folder and run:
    ```bash
    git init
    ```

2.  **Add Files**:
    ```bash
    git add .
    ```

3.  **Commit Changes**:
    ```bash
    git commit -m "Initial commit of AI Trading Dashboard v3.0"
    ```

4.  **Connect to GitHubRepo**:
    -   Go to [GitHub.com](https://github.com) and create a **New Repository**.
    -   Copy the URL (e.g., `https://github.com/YOUR_USER/YOUR_REPO_NAME.git`).
    -   Run this command (replace user/repo):
        ```bash
        git remote add origin https://github.com/YOUR_USER/YOUR_REPO_NAME.git
        git branch -M main
        git push -u origin main
        ```

## 🌐 Deployment
This app is ready for **Streamlit Cloud** or **Render**.

### Streamlit Cloud (Fastest)
1.  Push code to GitHub (see above).
2.  Go to [Streamlit Cloud](https://share.streamlit.io/).
3.  Select your repo and `app.py`.
4.  Click **Deploy**.

## 📂 Project Structure
-   `app.py`: Main dashboard application.
-   `utils/`:
    -   `market_data.py`: Fetches Stocks, Options, & Currencies.
    -   `indicators.py`: Calculates RSI, MACD, Signals.
    -   `visuals.py`: Generates Plotly Charts.
    -   `ai_engine.py`: Manages LSTM Model.
-   `train_model.py`: Script to retrain the AI.
-   `Latest_stock_price_model.keras`: Trained Model file.
