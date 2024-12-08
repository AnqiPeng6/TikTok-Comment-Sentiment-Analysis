# TikTok-Comment-Sentiment-Analysis
COMP400 McGill
TikTok Comment Sentiment Analysis is a custom-built software designed to classify TikTok comments into three sentiment categories: positive, negative, or neutral. The system processes comments by parsing them into individual words and word pairs, assigning sentiment scores using predefined sentiment dictionaries (sentiment_word.json and sentiment_word_pair.json) and a custom Word2Vec-based sentiment mapping approach.
The software continuously adapts by retraining its Word2Vec model with trending TikTok comments retrieved using a custom TikTok API built upon David Teather's unofficial TikTokApi. This enables real-time sentiment analysis, keeping the system relevant in TikTok's dynamic and evolving linguistic environment.
