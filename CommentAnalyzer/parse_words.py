import json  # Import JSON for saving and loading processed comments
from TikTokApi import TikTokApi
import asyncio
from transformers import pipeline
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from Word2Vec.word2vec import (
    update_word2vec_model,
    update_trending_comments,
    update_hashtag_comments,
    load_word2vec_model
)
#from word2vec import word2vec 
#import update_word2vec_model, update_trending_comments, load_word2vec_model


# Initialize the sentiment analyzer

script_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the processed_comments.json file
filepath = os.path.join(script_directory, "processed_comments.json")


processed_comments = []


# Function to load processed comments from a file
def get_sentiment_for_word(word, file_path = os.path.join(script_directory, "sentiment_word.json")):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
                existing_results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_results = {}
    score = 2.0
        # Build a set of existing words for faster lookup
    #existing_words = set(word for result in existing_results for word in result.keys())
    if word in existing_results:
        score = existing_results[word]
    else:
        model = load_word2vec_model()
        similar_words = check_words_in_word2vec(word, model)
        weighted_score = 0.0
        distances = []
        weights = []

        if similar_words:
            # Filter and process the first 3 similar words with distance > 0.4
            filtered_similar_words = [
                (similar_word, distance)
                for similar_word, distance in similar_words
                if similar_word in existing_results and distance > 0.4
            ][:3]

            # Compute weights and score if we have up to 3 valid similar words
            if len(filtered_similar_words) > 0:
                total_distance = sum(distance for _, distance in filtered_similar_words)

                for similar_word, distance in filtered_similar_words:
                    weight = (existing_results[similar_word] * distance) / total_distance
                    weights.append(weight)

                weighted_score = sum(weights)
                score = weighted_score
                
                existing_results[word] = score
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump(existing_results, file, ensure_ascii=False, indent=4)
                    print(f"Updated sentiment_word.json with: {word} -> {score}")
                except Exception as e:
                    print(f"Error saving updated sentiment_word.json: {e}")
                
            else:
                score = 2.0  # No valid similar words, retain default score
        
        
    
    return score

def get_sentiment_for_word_pair(word, file_path = os.path.join(script_directory, "sentiment_word_pair.json")):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
                existing_results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_results = {}
    score = 2.0
        # Build a set of existing words for faster lookup
    #existing_words = set(word for result in existing_results for word in result.keys())
    if word in existing_results:
        score = existing_results[word]
    else:
        # model = load_word2vec_model()
        # similar_words = check_words_in_word2vec(word, model)
        # if similar_words:
        #     for similar_word in similar_words:
        #         if similar_word in existing_results:
        #             score = existing_results[similar_word]
        #             break
        # else:
        score = 2.0
    
    return score

def load_processed_comments(file_path = filepath):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            processed_comments = json.load(file)
    except FileNotFoundError:
        processed_comments = []  # If the file doesn't exist, start with an empty list
    return processed_comments



def check_words_in_word2vec(word, word2vec_model):
    """
    Check if each word in each comment exists in the Word2Vec model.

    Parameters:
        processed_comments (list of list of str): List of comments, where each comment is a list of words.
        word2vec (Word2Vec): Trained Word2Vec model.

    Returns:
        list of dict: Each dictionary contains the comment and the presence status of each word.
    """
    
    results = []

    
            # Check if the word exists in the Word2Vec vocabulary
    if word in word2vec_model.wv.key_to_index:
        results = word2vec_model.wv.most_similar(word, topn=25)
                
            
        

    return results

# def save_sentiment_analysis_results(new_results, file_path = filepath):
#     """
#     Save sentiment analysis results to a JSON file as a single dictionary, ensuring no duplicate words are added.

#     Args:
#         new_results (list): A list of dictionaries containing sentiment scores for each comment.
#         file_path (str): Path to the JSON file for saving results.
#                          Default is 'sentiment_analysis_results.json'.
#     """
#     from nltk.sentiment import SentimentIntensityAnalyzer

#     sid = SentimentIntensityAnalyzer()
#     try:
#         # Load existing data if the file exists
#         try:
#             with open(file_path, "r", encoding="utf-8") as file:
#                 existing_results = json.load(file)
#         except (FileNotFoundError, json.JSONDecodeError):
#             existing_results = {}  # Initialize as an empty dictionary if file not found or invalid

#         # Filter new results to include only words not already in the file
#         for comment in new_results:
#             for word in comment:
#                 if word not in existing_results:  # Check if the word is already in the dictionary
#                     score = sid.polarity_scores(word)["compound"]
#                     existing_results[word] = score  # Add new word with its sentiment score

#         # Save updated results back to the file
#         with open(file_path, "w", encoding="utf-8") as file:
#             json.dump(existing_results, file, ensure_ascii=False, indent=4)
#         print(f"Sentiment analysis results successfully saved to '{file_path}'")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")



def load_sentiment_analysis_results(file_path = os.path.join(script_directory, "sentiment_word.json")):
    """
    Load sentiment analysis results from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing sentiment analysis results.
                         Default is 'sentiment_analysis_results.json'.

    Returns:
        list: A list of dictionaries containing the sentiment scores for each comment.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            results = json.load(file)
        print(f"Sentiment analysis results successfully loaded from '{file_path}'")
        return results
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from file '{file_path}'.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def get_sentiment(word):
    existing_results = {"joyful": 9, "elated": 2, "content": 7}
    score = 2.0
        # Build a set of existing words for faster lookup
    #existing_words = set(word for result in existing_results for word in result.keys())
    if word in existing_results:
        score = existing_results[word]
    else:
        model = load_word2vec_model()
        #similar_words = check_words_in_word2vec(word, model)
        similar_words = {
    "joyful": 0.5,
    "cheerful": 0.5,
    "content": 0.5,
    "elated": 0.5
        }
        weighted_score = 0.0
        distances = []
        weights = []

        if similar_words:
            # Filter and process the first 3 similar words with distance > 0.4
            filtered_similar_words = [
                (similar_word, distance)
                for similar_word, distance in similar_words.items()
                if similar_word in existing_results and distance > 0.4
            ][:3]

            # Compute weights and score if we have up to 3 valid similar words
            if len(filtered_similar_words) > 0:
                total_distance = sum(distance for _, distance in filtered_similar_words)

                for similar_word, distance in filtered_similar_words:
                    weight = (existing_results[similar_word] * distance) / total_distance
                    weights.append(weight)

                weighted_score = sum(weights)
                score = weighted_score
            else:
                score = 2.0  # No valid similar words, retain default score
    
    return score

def print_list_length(my_list):
    """
    Print the number of entries in the provided list.
    
    Args:
    my_list (list): A list whose entries are to be counted.
    """
    # Calculate the length of the list
    length = len(my_list)
    # Print the length of the list
    print(f"The list contains {length} entries.")
    
async def main():
    # # Load processed comments
    # processed_comments = load_processed_comments()
    # #save_sentiment_analysis_results(processed_comments)
    # sentiment_results = load_sentiment_analysis_results()
    # if sentiment_results:
    #     print("Loaded Sentiment Results:", sentiment_results)
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the processed_comments.json file
    filepath = os.path.join(script_directory, "comment_sentiment_score.json")
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            processed_comments = json.load(file)
    except FileNotFoundError:
        processed_comments = []  # If the file doesn't exist, start with an empty list
        
    print_list_length(processed_comments)
    

if __name__ == "__main__":
    # Uncomment to run the async main function
    asyncio.run(main())