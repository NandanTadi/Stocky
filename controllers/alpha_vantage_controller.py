import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

BASE_URL = "https://www.alphavantage.co/query"

def get_stock_details(ticker):
    params = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Name" in data:
            return data
        else:
            return {"error": "No data found for the given ticker. Please check the symbol."}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_stock_time_series(ticker):
    params = {
        "function": "TIME_SERIES_DAILY",  # AlphaVantage function for daily time series
        "symbol": ticker,
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        data = response.json()
        
        # Check if the response contains the expected data
        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]
        else:
            return {"error": "No time series data found for the given ticker. Please check the symbol."}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_news_sentiment(ticker, sort="LATEST", time_from=None, time_to=None, limit=25):
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "sort": sort,
        "limit": limit,
        "apikey": API_KEY
    }
    if time_from:
        params["time_from"] = time_from
    if time_to:
        params["time_to"] = time_to
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if "feed" in data:
            return data["feed"]
        else:
            return {"error": data.get("message", "No data available for the given parameters.")}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    ticker = input("Enter stock ticker (e.g., AAPL, TSLA): ").strip()
    stock_details = get_stock_details(ticker)
    print(stock_details)
