import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_stock_chart(df, ticker, show_indicators=True):
    """
    Creates a professional Candlestick chart with Volume and Indicators.
    """
    if df.empty:
        return go.Figure()

    # Create subplots: Price on Row 1, Volume on Row 2
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.7, 0.3])

    # Candlestick
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name=f'{ticker} Price'),
                  row=1, col=1)

    # Moving Averages
    if show_indicators:
        if 'SMA_50' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='orange', width=1), name='SMA 50'), row=1, col=1)
        if 'SMA_200' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], line=dict(color='blue', width=1), name='SMA 200'), row=1, col=1)
        if 'BB_Upper' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], line=dict(color='gray', width=1, dash='dot'), showlegend=False), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], line=dict(color='gray', width=1, dash='dot'), fill='tonexty', fillcolor='rgba(128,128,128,0.1)', name='Bollinger Bands'), row=1, col=1)

    # Volume
    colors = ['green' if row['Open'] - row['Close'] >= 0 else 'red' for index, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Volume'), row=2, col=1)

    # Layout
    fig.update_layout(
        title=f'{ticker} Professional Analysis',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        height=600,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_prediction_chart(history_df, pred_df, ticker):
    """
    Overlays AI predictions on recent history.
    """
    fig = go.Figure()
    
    # Historical Data (Last 100 points for context)
    recent_history = history_df.tail(100)
    fig.add_trace(go.Scatter(x=recent_history.index, y=recent_history['Close'], 
                             mode='lines', name='Historical Data'))
    
    # Prediction
    fig.add_trace(go.Scatter(x=pred_df.index, y=pred_df['Predicted Price'], 
                             mode='lines+markers', line=dict(color='cyan', width=2), name='AI Forecast'))
    
    fig.update_layout(
        title=f'{ticker} AI Prediction Trail',
        template="plotly_dark",
        height=500
    )
    return fig
