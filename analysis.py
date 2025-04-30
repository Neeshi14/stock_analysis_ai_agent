import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

def calculate_indicators(data):
    close = data['Close']

    # 50-day and 200-day SMA
    data['SMA50'] = close.rolling(window=50).mean()
    data['SMA100'] = close.rolling(window=100).mean()

    # RSI
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    roll_up = gain.rolling(window=14).mean()
    roll_down = loss.rolling(window=14).mean()
    rs = roll_up / roll_down
    data['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    data['MACD'] = ema_12 - ema_26
    data['MACD_signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    return data

def plot_stock_data(data, symbol):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), height_ratios=[3, 1, 1])

    # Price and SMA
    ax1.plot(data.index, data['Close'], label='Close Price', color='blue')
    ax1.plot(data.index, data['SMA50'], label='50-day SMA', color='orange', alpha=0.7)
    ax1.plot(data.index, data['SMA100'], label='200-day SMA', color='red', alpha=0.7)
    ax1.set_title(f'{symbol} Stock Analysis')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylabel('Price')
    ax1.set_xlabel('Date')

    # RSI
    ax2.plot(data.index, data['RSI'], label='RSI', color='purple')
    ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5)
    ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5)
    ax2.set_ylim([0, 100])
    ax2.legend()
    ax2.grid(True)
    ax2.set_ylabel('RSI')
    ax2.set_xlabel('Date')
    ax2.set_title('Relative Strength Index (RSI)')

    # MACD
    ax3.plot(data.index, data['MACD'], label='MACD', color='blue')
    ax3.plot(data.index, data['MACD_signal'], label='Signal', color='red')
    ax3.legend()
    ax3.grid(True)
    ax3.set_ylabel('MACD')
    ax3.set_xlabel('Date')
    ax3.set_title('MACD Indicator')

    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    plt.tight_layout()

    if not os.path.exists('static/plots'):
        os.makedirs('static/plots')

    plot_path = f'static/plots/{symbol}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(plot_path)
    plt.close()
    plt.show()

    return plot_path

def fetch_stock_data(symbol, timeframe):
    try:
        period_map = {
            "1 month": "1mo",
            "6 months": "6mo",
            "1 year": "1y"
        }

        period = period_map.get(timeframe, "1mo")

        # Download data
        data = yf.download(symbol, period=period, interval="1d", progress=False, auto_adjust=False)

        if data.empty:
            raise ValueError("No data found for the given symbol/timeframe.")

        data = calculate_indicators(data)

        latest_rsi = data["RSI"].dropna().iloc[-1] if not data["RSI"].dropna().empty else "N/A"
        latest_macd = data["MACD"].dropna().iloc[-1] if not data["MACD"].dropna().empty else "N/A"
        sma50 = data["SMA50"].dropna().iloc[-1] if not data["SMA50"].dropna().empty else "N/A"
        sma100 = data["SMA100"].dropna().iloc[-1] if not data["SMA100"].dropna().empty else "N/A"

        summary = f"""
        RSI: {latest_rsi}
        MACD: {latest_macd}
        50-day SMA: {sma50}
        200-day SMA: {sma100}
        Latest Close Price: {data['Close'].iloc[-1]}
        """

        plot_path = plot_stock_data(data, symbol)

        return latest_rsi, latest_macd, sma50, sma100, summary, plot_path

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return "N/A", "N/A", "N/A", "N/A", f"Data fetch error: {str(e)}", None

# Example usage (uncomment to test):
#result = fetch_stock_data("GOOGL", "1 month")
#print(result)
