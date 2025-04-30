from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain

# Gemini API key
GEMINI_API_KEY = "AIzaSyB10uqRhByF1fVpFzNdMEU79vWfGmD2DBg"

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.5
)

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["stock_symbol", "timeframe", "rsi", "macd", "sma50", "sma100", "summary"],
    template="""
You are an experienced financial analyst AI.

A user is analyzing the stock symbol "{stock_symbol}" for a timeframe of {timeframe}.

Below is the data:
- RSI: {rsi}
- MACD: {macd}
- 50-day SMA: {sma50}
- 100-day SMA: {sma100}
- Summary Stats: {summary}

Based on these technical indicators and your financial knowledge:
1. Should the user BUY, SELL, or HOLD this stock?
2. Provide a confidence score from 0 to 100.
3. Briefly explain your reasoning using the indicators.

Output must follow this format strictly:
---
Recommendation: <Buy/Sell/Hold>
Confidence Score: <score>
Explanation: <1-2 sentence explanation>

show the plot of the stock data with the indicators.
---
"""
)

# Define the chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Callable function
def analyze_stock(stock_symbol, timeframe, rsi, macd, sma50, sma100, summary):
    response = chain.run({
        "stock_symbol": stock_symbol,
        "timeframe": timeframe,
        "rsi": rsi,
        "macd": macd,
        "sma50": sma50,
        "sma100": sma100,
        "summary": summary
    })
    return response
