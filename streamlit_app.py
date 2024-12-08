import streamlit as st
from webpages.home import stocky_page
from webpages.stockylze import stocklyze_page

# Sidebar for page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Stocklyze"])

# Render the selected page
if page == "Home":
    stocky_page()
elif page == "Stocklyze":
    stocklyze_page()
