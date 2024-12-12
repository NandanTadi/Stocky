import streamlit as st
import pandas as pd
from controllers.alpha_vantage_controller import get_news_sentiment
from core.utils import dateToString, formatDateToHuman
from bs4 import BeautifulSoup
import requests

def scrape_article_text(url):
    """Fetch and extract the full text of an article from its URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract article paragraphs (customize based on website structure)
        paragraphs = soup.find_all('p')
        content = ' '.join(paragraph.text for paragraph in paragraphs)
        return content if content else "Unable to extract content."
    except requests.RequestException as e:
        return f"Error fetching the article: {e}"

def stocklyze_page():
    st.title("Stocklyze \U0001F9E0")
    st.write("Analyze live and historical market news sentiment for your selected stock ticker.")

    # User inputs
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):")
    sort_by = st.selectbox("Sort By", ["LATEST", "EARLIEST", "RELEVANCE"])
    time_from = st.date_input("Select Start Date (optional)")
    time_to = st.date_input("Select End Date (optional)")
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
                # Process and display data in a structured format
                articles = []
                for article in news_data:
                    full_text = scrape_article_text(article["url"])
                    articles.append({
                        "Title": article["title"],
                        "Source": article["source"],
                        "Published At": formatDateToHuman(article["time_published"]),
                        "Relevance Score": max(
                            float(topic["relevance_score"]) for topic in article["topics"]
                        ),
                        "Overall Sentiment": article["overall_sentiment_label"],
                        "Summary": article["summary"],
                        "Full Text": full_text,
                        "URL": article["url"]
                    })

                # Convert articles to a DataFrame for sentiment analysis
                df = pd.DataFrame(articles)

                # Dropdown to filter by source
                sources = df["Source"].unique().tolist()
                selected_source = st.selectbox("Filter by Source", ["All Sources"] + sources)
                if selected_source != "All Sources":
                    df = df[df["Source"] == selected_source]

                # Display articles in a table
                st.subheader(f"News Sentiment for {ticker.upper()}")
                st.dataframe(df[["Title", "Source", "Published At", "Relevance Score", "Overall Sentiment"]])

                # Structured data for sentiment analysis
                sentiment_data = df.to_dict(orient='records')

                # Option to view full article
                st.write("---")
                for _, row in df.iterrows():
                    st.write(f"### {row['Title']}")
                    st.write(f"**Source**: {row['Source']}")
                    st.write(f"**Published At**: {row['Published At']}")
                    st.write(f"**Relevance Score**: {row['Relevance Score']}")
                    st.write(f"**Overall Sentiment**: {row['Overall Sentiment']}")
                    st.write(f"**Summary**: {row['Summary']}")

                    if st.button(f"Read Full Text: {row['Title']}", key=row['Title']):
                        st.write(f"**Full Text**: {row['Full Text']}")
                    st.markdown(f"[Read Original Article]({row['URL']})")
                    st.write("---")

                # Display sentiment data for analysis
                st.write("### Structured Data for Sentiment Analysis")
                st.json(sentiment_data)
        else:
            st.warning("Please enter a valid stock ticker.")
