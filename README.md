# 🎈 Blank App Template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run streamlit_app.py
   ```

---

### File Documentation

#### 1. `streamlit_app.py`
   - Main entry point of the application.
   - Manages the navigation between different pages ("Home" and "Stocklyze").
   - Imports `stocky_page` from `webpages.home` and `stocklyze_page` from `webpages.stockylze` to display their respective content.

#### 2. `home.py`
   - Defines the `stocky_page` function, which implements the "Home" page.
   - Allows users to input a stock ticker to analyze market sentiment.
   - Fetches and displays stock details (e.g., sector, industry) and a stock price chart using Alpha Vantage API.

#### 3. `stockylze.py`
   - Implements the "Stocklyze" page using the `stocklyze_page` function.
   - Lets users fetch live and historical news sentiment for a given stock ticker.
   - Integrates FinBERT for sentiment analysis, and allows users to customize sentiment scores with keywords.
   - Uses the `predict` function from `stockylzePredicter.py` to predict stock movement.

#### 4. `alpha_vantage_controller.py`
   - Provides API integration for fetching stock details and time-series data from Alpha Vantage.
   - Includes functions:
     - `get_stock_details`: Fetches stock metadata like name, sector, and industry.
     - `get_stock_time_series`: Retrieves daily stock time series data.
     - `get_news_sentiment`: Fetches news sentiment for a stock ticker.

#### 5. `customModel.py`
   - Defines `calculate_custom_sentiment` to compute sentiment scores based on user-defined keywords (positive, neutral, negative).
   - Calculates scores as percentages and assigns a sentiment label.

#### 6. `service.py`
   - Implements utility functions for text scraping and sentiment analysis:
     - `scrape_article_text`: Extracts article text from a URL.
     - `get_sentiment_pipeline`: Initializes a FinBERT pipeline for sentiment analysis.

#### 7. `stockylzePredicter.py`
   - Defines the `predict` function, which calculates a weighted sentiment score using FinBERT and custom sentiment data.
   - Predicts stock movement trends based on the weighted score:
     - "Likely to Increase"
     - "Likely to Decrease"
     - "Neutral".

#### 8. `utils.py`
   - Contains utility functions for date formatting:
     - `dateToString`: Converts a `datetime` object to a string in the required API format.
     - `formatDateToHuman`: Converts an API-formatted date string to a human-readable format.

---

### Features

- **Stock Metadata and Charting**: Fetches stock details and displays daily price charts.
- **News Sentiment Analysis**:
  - Uses FinBERT for pre-trained sentiment analysis.
  - Allows users to customize sentiment scoring with keywords.
- **Prediction**: Provides stock movement predictions based on sentiment analysis.
- **Interactive Visualization**: Uses Streamlit for an intuitive and interactive experience.

### Prerequisites

- Obtain an API key from [Alpha Vantage](https://www.alphavantage.co/) and add it to `secrets.toml` as `ALPHA_VANTAGE_API_KEY`.
- Ensure Python 3.8+ is installed.
