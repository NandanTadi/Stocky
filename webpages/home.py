import streamlit as st
import pandas as pd
from controllers.alpha_vantage_controller import get_stock_details, get_stock_time_series

def stocky_page():
    st.title("Stocky 📈")
    st.write("Analyze market sentiment for your favorite stocks with ease! Enter a stock ticker to retrieve relevant research papers and get a quick, summarized sentiment score based on keyword analysis.")

    # Input box for stock ticker
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):")

    if st.button("Submit"):
        if ticker:
            # Fetch stock details
            stock_details = get_stock_details(ticker)
            time_series = get_stock_time_series(ticker)
            
            # Display stock details
            if "error" in stock_details:
                st.error(stock_details["error"])
            else:
                st.success(f"Details for {stock_details['Name']} ({stock_details['Symbol']})")
                st.write(f"**Sector**: {stock_details.get('Sector', 'N/A')}")
                st.write(f"**Industry**: {stock_details.get('Industry', 'N/A')}")
                st.write(f"**Description**: {stock_details.get('Description', 'N/A')}")

            # Display stock chart
            if "error" in time_series:
                st.error(time_series["error"])
            else:
                # Convert the time series data into a Pandas DataFrame
                df = pd.DataFrame.from_dict(time_series, orient="index")
                df = df.rename(columns={
                    "1. open": "Open",
                    "2. high": "High",
                    "3. low": "Low",
                    "4. close": "Close",
                    "5. volume": "Volume"
                }).astype(float)

                # Reverse the DataFrame to show oldest data first
                df = df.iloc[::-1]

                # Plot the closing price
                st.subheader(f"{ticker.upper()} Stock Price (Daily)")
                st.line_chart(df["Close"])
        else:
            st.warning("Please enter a valid stock ticker.")
