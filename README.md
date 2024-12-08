# TikTok-Comment-Sentiment-Analysis
COMP400 McGill
TikTok Comment Sentiment Analysis is a custom-built software designed to classify TikTok comments into three sentiment categories: positive, negative, or neutral. The system processes comments by parsing them into individual words and word pairs, assigning sentiment scores using predefined sentiment dictionaries (sentiment_word.json and sentiment_word_pair.json) and a custom Word2Vec-based sentiment mapping approach.
The software continuously adapts by retraining its Word2Vec model with trending TikTok comments retrieved using a custom TikTok API built upon David Teather's unofficial TikTokApi. This enables real-time sentiment analysis, keeping the system relevant in TikTok's dynamic and evolving linguistic environment.
## **Key Features**
* **Sentiment Classification**: Automatically classifies TikTok comments as positive, negative, or neutral, ensuring sentiment-based categorization for text analysis.

* **Predefined Dictionaries**: Utilizes two sentiment dictionaries:
  * `sentiment_word.json` for single words.
  * `sentiment_word_pair.json` for word pairs.

* **Word2Vec Integration**: Leverages a custom-trained Word2Vec model, originally retrieved from Gensim, to infer sentiment scores for previously unseen words by learning from TikTok comment trends.

* **Automatic Updates**: Continuously retrains the Word2Vec model using recent TikTok comments retrieved via the custom TikTok API and updates word-to-sentiment mappings accordingly.

* **Result Comparison**: Evaluates system performance by comparing results against manually annotated datasets and sentiment analysis results from BERT-based models for benchmarking.

# Installation

## 1. Clone the Repository
Clone the TikTok Comment Sentiment Analysis repository into your local machine:
```bash
git clone https://github.com/AnqiPeng6/TikTok-Comment-Sentiment-Analysis.git
cd TikTok-Comment-Sentiment-Analysis

## 1. Set Up the Virtual Environment
To manage dependencies effectively, it's recommended to use a virtual environment:
```bash
# On Unix-based systems:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

