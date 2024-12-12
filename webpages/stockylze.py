import streamlit as st
import pandas as pd
from controllers.alpha_vantage_controller import get_news_sentiment
from core.utils import dateToString, formatDateToHuman
from core.service import scrape_article_text, get_sentiment_pipeline
from bs4 import BeautifulSoup
import requests

sentiment_pipeline = get_sentiment_pipeline()

def stocklyze_page():
    st.title("Stocklyze \U0001F9E0")
    st.write("Analyze live and historical market news sentiment for your selected stock ticker.")

    # User inputs
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):")
    sort_by = st.selectbox("Sort By", ["LATEST", "EARLIEST", "RELEVANCE"])
    time_from = st.date_input("Select Start Date (optional)")
    time_to = st.date_input("Select End Date (optional)")
    limit = st.slider("Limit Results", 50, 100, 50)

    # Convert dates to API-compatible strings
    time_from_str = time_from.strftime("%Y%m%dT%H%M") if time_from else None
    time_to_str = time_to.strftime("%Y%m%dT%H%M") if time_to else None

    if st.button("Fetch News Sentiment"):
        if ticker:
            # Indicate loading process
            with st.spinner("Fetching and analyzing articles..."):
                # Fetch news sentiment data
                news_data = get_news_sentiment(ticker, sort_by, time_from_str, time_to_str, limit)

                if "error" in news_data:
                    st.error(news_data["error"])
                else:
                    # Process and display data in a structured format
                    articles = []
                    for article in news_data:
                        # Scrape full text
                        full_text = scrape_article_text(article["url"])

                        # Analyze sentiment using FinBERT
                        sentiment = sentiment_pipeline(full_text[:512])  # Truncate text to 512 tokens
                        sentiment_label = sentiment[0]["label"]
                        sentiment_score = sentiment[0]["score"]

                        # Prepare article data
                        articles.append({
                            "Title": article["title"],
                            "Source": article["source"],
                            "Published At": formatDateToHuman(article["time_published"]),
                            "Relevance Score": max(
                                float(topic["relevance_score"]) for topic in article["topics"]
                            ),
                            "Sentiment Label": sentiment_label,
                            "Sentiment Score": sentiment_score,
                            "Summary": article["summary"],
                            "Full Text": full_text,
                            "URL": article["url"]
                        })

                    # Convert articles to a DataFrame
                    df = pd.DataFrame(articles)

                    # Display detailed sentiment analysis for each article
                    st.subheader(f"News Sentiment for {ticker.upper()}")
                    for _, row in df.iterrows():
                        st.write(f"### {row['Title']}")
                        st.write(f"**Source**: {row['Source']}")
                        st.write(f"**Published At**: {row['Published At']}")
                        st.write(f"**Relevance Score**: {row['Relevance Score']}")
                        st.write(f"**Sentiment Label**: {row['Sentiment Label']} (Score: {row['Sentiment Score']:.2f})")
                        st.write(f"**Summary**: {row['Summary']}")
                        st.write(f"**Full Text**: {row['Full Text'][:500]}...")  # Show only first 500 characters
                        st.markdown(f"[Read Original Article]({row['URL']})")
                        st.write("---")

                    # Display full DataFrame for summary view
                    st.subheader("Summary Table")
                    st.dataframe(df[["Title", "Source", "Published At", "Relevance Score", "Sentiment Label", "Sentiment Score"]])
        else:
            st.warning("Please enter a valid stock ticker.")