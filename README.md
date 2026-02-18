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
    git clone https://github.com/DevrajOO7/Stock_prediction_AI.git
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
-   **Run the App**:
    -   Double-click `run_app.bat` (Windows).
    -   Or run: `streamlit run app.py`


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
## Screenshot

<img width="1920" height="1032" alt="AI Trading Desk · Streamlit - Google Chrome 18-02-2026 15_08_13" src="https://github.com/user-attachments/assets/c300afb7-29aa-4921-8a8c-19b4f1c4df40" />

<img width="1920" height="1032" alt="AI Trading Desk · Streamlit - Google Chrome 18-02-2026 15_04_41" src="https://github.com/user-attachments/assets/3e35e9c5-5efe-4872-8ddf-6f5ade5d654a" />

<img width="1920" height="1032" alt="AI Trading Desk · Streamlit - Google Chrome 18-02-2026 15_04_25" src="https://github.com/user-attachments/assets/b3a8dd57-7fb9-4735-b052-62f87e9a3f98" />

<img width="1920" height="1032" alt="AI Trading Desk · Streamlit - Google Chrome 18-02-2026 15_04_14" src="https://github.com/user-attachments/assets/f7111813-696b-440a-bd93-5c8c6af802f1" />

<img width="1920" height="1032" alt="AI Trading Desk · Streamlit - Google Chrome 18-02-2026 15_03_54" src="https://github.com/user-attachments/assets/759340bd-6f6f-447c-8965-04e79ce15c99" />


