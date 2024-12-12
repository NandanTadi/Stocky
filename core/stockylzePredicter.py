
def predict(sentiments, relevance_scores, custom_sentiments=None):
    # Calculate weighted sentiment score using FinBERT
    weighted_sentiment = sum(s * r for s, r in zip(sentiments, relevance_scores))
    total_relevance = sum(relevance_scores)
    final_score = weighted_sentiment / total_relevance if total_relevance > 0 else 0

    # If custom sentiments are provided, combine them
    if custom_sentiments:
        custom_positive = sum(cs["Positive Score"] * r for cs, r in zip(custom_sentiments, relevance_scores))
        custom_negative = sum(cs["Negative Score"] * r for cs, r in zip(custom_sentiments, relevance_scores))
        final_score = custom_positive - custom_negative

    # Determine prediction based on final score
    if final_score > 0.05:  # Adjust threshold as needed
        prediction = "Likely to Increase"
    elif final_score < -0.05:
        prediction = "Likely to Decrease"
    else:
        prediction = "Neutral"

    return {
        "prediction": prediction,
        "final_score": final_score
    }
