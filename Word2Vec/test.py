from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# List of words to analyze
words_list = ["perfect", "terrible", "happy", "sad", "beautiful", "ugly", "positive", "negative", "good", "bad"]

# Calculate sentiment scores
sentiments = {word: sid.polarity_scores(word)["compound"] for word in words_list}
print(sentiments)