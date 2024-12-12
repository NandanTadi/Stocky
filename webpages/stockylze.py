import streamlit as st
import pandas as pd
from controllers.alpha_vantage_controller import get_news_sentiment
from core.utils import dateToString, formatDateToHuman
from core.service import scrape_article_text, get_sentiment_pipeline
from core.customModel import calculate_custom_sentiment
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

    # Custom Sentiment Fields
    st.write("### Customize Sentiment Analysis")
    positive_keywords = st.text_input("Enter Positive Keywords (comma-separated)").split(",")
    neutral_keywords = st.text_input("Enter Neutral Keywords (comma-separated)").split(",")
    negative_keywords = st.text_input("Enter Negative Keywords (comma-separated)").split(",")

    # Convert dates to API-compatible strings
    time_from_str = time_from.strftime("%Y%m%dT%H%M") if time_from else None
    time_to_str = time_to.strftime("%Y%m%dT%H%M") if time_to else None

    if st.button("Fetch News Sentiment"):
        if ticker:
            with st.spinner("Fetching and analyzing articles..."):
                news_data = get_news_sentiment(ticker, sort_by, time_from_str, time_to_str, limit)

                if "error" in news_data:
                    st.error(news_data["error"])
                else:
                    articles = []
                    for article in news_data:
                        full_text = scrape_article_text(article["url"])
                        sentiment = sentiment_pipeline(full_text[:512])  # Truncate text to 512 tokens
                        sentiment_label = sentiment[0]["label"]
                        sentiment_score = sentiment[0]["score"]

                        # Calculate custom sentiment
                        custom_label, custom_scores = calculate_custom_sentiment(
                            full_text, positive_keywords, neutral_keywords, negative_keywords
                        )

                        articles.append({
                            "Title": article["title"],
                            "Source": article["source"],
                            "Published At": formatDateToHuman(article["time_published"]),
                            "Relevance Score": max(
                                float(topic["relevance_score"]) for topic in article["topics"]
                            ),
                            "FinBERT Sentiment Label": sentiment_label,
                            "FinBERT Sentiment Score": sentiment_score,
                            "Custom Sentiment Label": custom_label,
                            "Custom Sentiment Scores": custom_scores,
                            "Summary": article["summary"],
                            "Full Text": full_text,
                            "URL": article["url"]
                        })

                    # Convert articles to DataFrame
                    df = pd.DataFrame(articles)

                    # Display detailed sentiment analysis for each article
                    st.subheader(f"News Sentiment for {ticker.upper()}")
                    for _, row in df.iterrows():
                        st.write(f"### {row['Title']}")
                        st.write(f"**Source**: {row['Source']}")
                        st.write(f"**Published At**: {row['Published At']}")
                        st.write(f"**Relevance Score**: {row['Relevance Score']}")
                        st.write(f"**FinBERT Sentiment Label**: {row['FinBERT Sentiment Label']} (Score: {row['FinBERT Sentiment Score']:.2f})")
                        st.write(f"**Custom Sentiment Label**: {row['Custom Sentiment Label']}")
                        st.write(f"**Custom Sentiment Scores**: {row['Custom Sentiment Scores']}")
                        st.write(f"**Summary**: {row['Summary']}")
                        st.write(f"**Full Text**: {row['Full Text'][:500]}...")  # Show only first 500 characters
                        st.markdown(f"[Read Original Article]({row['URL']})")
                        st.write("---")

                    # Display full DataFrame for summary view
                    st.subheader("Summary Table")
                    st.dataframe(df[[
                        "Title", "Source", "Published At", "Relevance Score",
                        "FinBERT Sentiment Label", "FinBERT Sentiment Score",
                        "Custom Sentiment Label"
                    ]])
        else:
            st.warning("Please enter a valid stock ticker.")