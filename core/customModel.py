import streamlit as st

def calculate_custom_sentiment(full_text, positive_keywords, neutral_keywords, negative_keywords):
    """Calculate custom sentiment based on user-defined keywords."""
    positive_count = sum(full_text.lower().count(keyword.strip()) for keyword in positive_keywords if keyword)
    neutral_count = sum(full_text.lower().count(keyword.strip()) for keyword in neutral_keywords if keyword)
    negative_count = sum(full_text.lower().count(keyword.strip()) for keyword in negative_keywords if keyword)
    
    total_count = positive_count + neutral_count + negative_count

    # Calculate sentiment scores
    if total_count > 0:
        positive_score = positive_count / total_count
        neutral_score = neutral_count / total_count
        negative_score = negative_count / total_count
    else:
        positive_score = neutral_score = negative_score = 0

    # Determine sentiment label
    if positive_score > max(neutral_score, negative_score):
        label = "Positive"
    elif negative_score > max(positive_score, neutral_score):
        label = "Negative"
    else:
        label = "Neutral"

    # Return custom sentiment results
    return label, {
        "Positive Score": positive_score,
        "Neutral Score": neutral_score,
        "Negative Score": negative_score
    }