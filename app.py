from flask import Flask, render_template, request
from analysis import fetch_stock_data
from agent import analyze_stock

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    stock_symbol = request.form['symbol']
    timeframe = request.form['timeframe']

    # Fetch stock data
    rsi, macd, sma50, sma100, summary, plot_path = fetch_stock_data(stock_symbol, timeframe)

    # Run agent analysis
    result = analyze_stock(stock_symbol, timeframe, rsi, macd, sma50, sma100, summary)

    # Parse agent result into structured dictionary
    output = {
        'symbol': stock_symbol.upper(),
        'timeframe': timeframe,
        'recommendation': '',
        'confidence': '',
        'explanation': '',
        'plot_path': plot_path
    }

    # Clean result output
    lines = [line.strip() for line in result.strip().split('\n') if line.strip()]
    for line in lines:
        if line.lower().startswith("recommendation:"):
            output['recommendation'] = line.split(":", 1)[1].strip()    
        elif line.lower().startswith("confidence score:"):
            output['confidence'] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("show the plot of the stock data with the indicators."):
            continue   
        elif line.lower().startswith("explanation:"):
            output['explanation'] = line.split(":", 1)[1].strip()

    return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
