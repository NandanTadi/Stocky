import streamlit as st
import pandas as pd
from controllers.alpha_vantage_controller import get_news_sentiment
from core.utils import dateToString, formatDateToHuman

def stocklyze_page():
    st.title("Stocklyze 🧠")
    st.write("Analyze live and historical market news sentiment for your selected stock ticker.")

    # User inputs
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):")
    sort_by = st.selectbox("Sort By", ["LATEST", "EARLIEST", "RELEVANCE"])
    time_from = st.date_input("Select Start Date (optional)")
    time_to = st.date_input("Select End Date (time_to)")
    limit = st.slider("Limit Results", 50, 100, 50)

    if time_from:
        time_from_str = time_from.strftime("%Y%m%dT%H%M")

    if time_to:
        time_to_str = time_to.strftime("%Y%m%dT%H%M")

    if st.button("Fetch News Sentiment"):
        if ticker:
            # Fetch news sentiment data
            news_data = get_news_sentiment(ticker, sort_by, time_from_str, time_to_str, limit)
            
            if "error" in news_data:
                st.error(news_data["error"])
            else:
                # Process and display data
                articles = []
                for article in news_data:
                    articles.append({
                        "Title": article["title"],
                        "Source": article["source"],
                        "Published At": formatDateToHuman(article["time_published"]),
                        "Relevance Score": max(
                            float(topic["relevance_score"]) for topic in article["topics"]
                        ),
                        "Overall Sentiment": article["overall_sentiment_label"],
                        "Summary": article["summary"],
                        "URL": article["url"]
                    })

                # Convert articles to DataFrame
                df = pd.DataFrame(articles)

                # Dropdown to filter by source
                sources = df["Source"].unique().tolist()
                selected_source = st.selectbox("Filter by Source", ["All Sources"] + sources)
                if selected_source != "All Sources":
                    df = df[df["Source"] == selected_source]

                # Display articles in a table
                st.subheader(f"News Sentiment for {ticker.upper()}")
                st.dataframe(df[["Title", "Source", "Published At", "Relevance Score", "Overall Sentiment"]])

                # Option to view full article
                st.write("---")
                for _, row in df.iterrows():
                    st.write(f"### {row['Title']}")
                    st.write(f"**Source**: {row['Source']}")
                    st.write(f"**Published At**: {row['Published At']}")
                    st.write(f"**Relevance Score**: {row['Relevance Score']}")
                    st.write(f"**Overall Sentiment**: {row['Overall Sentiment']}")
                    st.write(f"**Summary**: {row['Summary']}")
                    st.markdown(f"[Read Full Article]({row['URL']})")
                    st.write("---")
        else:
            st.warning("Please enter a valid stock ticker.")
