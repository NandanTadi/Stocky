import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from transformers import pipeline

    
@st.cache_resource
def get_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

def scrape_article_text(url):
    """Fetch and extract the full text of an article from its URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    full_text = '\n'.join(para.get_text() for para in soup.find_all('p'))
    return full_text or "No content available."
