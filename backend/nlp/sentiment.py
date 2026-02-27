from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    if not text:
        return {
            "compound": 0.0,
            "polarity": 0.0,
            "combined": 0.0,
            "confidence": 0.0,
            "raw": {"vader": {}, "textblob": {}}
        }

    vader_scores = analyzer.polarity_scores(text)
    tb = TextBlob(text)
    tb_polarity = max(-1.0, min(1.0, tb.sentiment.polarity))

    length = len(text.strip())
    if length < 40:
        w_vader, w_tb = 0.75, 0.25
    else:
        w_vader, w_tb = 0.6, 0.4

    combined = (w_vader * vader_scores["compound"]) + (w_tb * tb_polarity)

    agreement = 1 - abs(vader_scores["compound"] - tb_polarity)  
    magnitude = min(1.0, abs(combined)) 
    confidence = max(0.15, min(1.0, (agreement + magnitude) / 2))  

    return {
        "compound": vader_scores["compound"],
        "polarity": tb_polarity,
        "combined": round(combined, 3),
        "confidence": round(confidence, 3),
        "raw": {"vader": vader_scores, "textblob": {"polarity": tb_polarity}}
    }
