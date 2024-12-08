from parse_words import get_sentiment_for_word, get_sentiment_for_word_pair, load_processed_comments
import json
from Word2Vec.word2vec import (
    update_word2vec_model,
    update_trending_comments,
    update_hashtag_comments,
    load_word2vec_model
)
def get_sentiment_for_comments(comments):
    results = []
    word2vec = load_word2vec_model()
    update_word2vec_model(word2vec, comments)
    for comment_words in comments:
        total_score = 0
        noted_words = 0
        used_indices = set()  # Track indices that are part of word pairs

        # Traverse through word pairs
        for i in range(len(comment_words) - 1):
            word_pair = f"{comment_words[i]} {comment_words[i + 1]}"
            score = get_sentiment_for_word_pair(word_pair)  # Ensure this function is correct
            if score != 2.0:
                total_score += score
                noted_words += 2  # Count both words in the pair
                used_indices.update([i, i + 1])  # Mark indices as used

        # Check individual words for sentiment
        for j, word in enumerate(comment_words):
            if j not in used_indices:  # Only process words not part of any pair
                score = get_sentiment_for_word(word)  # Ensure this function is correct
                if score != 2.0:
                    total_score += score
                    noted_words += 1

        # Avoid division by zero
       
        average_sentiment = total_score / noted_words if noted_words > 0 else 0
        results.append(average_sentiment)

    return results

def print_sentiment_results(comments, results):
    for comment, score in zip(comments, results):
        # Determine the sentiment result
        if score > 0:
            sentiment = "positive"
        elif score < 0:
            sentiment = "negative"
        elif score == 0:
            sentiment = "neutral"
        
        # Print the comment and its result
        print(f"Comment: {' '.join(comment)}")
        print(f"Result: {sentiment}")
        print()  # Blank line for better readability
        
import os
import json

def save_to_comment_sentiment_score(comments, results):
    """
    Saves the input data into a file named 'comment_sentiment_score.json'
    in the same format as printed results.
    
    Args:
        comments: List of comments (each as a list of words).
        results: List of sentiment scores corresponding to the comments.
    """
    # Prepare the data in the same format as the printed output
    data_to_save = []
    for comment, score in zip(comments, results):
        # Determine the sentiment result
        if score > 0:
            sentiment = "positive"
        elif score < 0:
            sentiment = "negative"
        elif score == 0:
            sentiment = "neutral"
        
        # Append the formatted result to the data list
        data_to_save.append({
            "comment": " ".join(comment),
            "result": sentiment,
            "score": score
        })
    
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path for the output file
    file_path = os.path.join(script_directory, "comment_sentiment_score.json")
    
    # Save the data to a JSON file
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

        
if __name__ == "__main__":
    comments = load_processed_comments()
    #comments = [["that's", "just", "not", "funny"]]
    existing_results2 = get_sentiment_for_comments(comments)
    
    save_to_comment_sentiment_score(comments, existing_results2)
