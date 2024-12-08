import json
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the processed_comments.json file
filepath = os.path.join(script_directory, "processed_comments.json")

def load_data(filename):
    """Load data from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def calculate_accuracy(truth, predictions):
    """Calculate the accuracy of predictions against the truth."""
    correct = 0
    total = len(truth)
    
    # Convert truth data to a dictionary with string comments as keys
    truth_dict = {}
    for item in truth:
        # Ensure the comment is a string
        comment = ' '.join(item['comment']) if isinstance(item['comment'], list) else item['comment']
        truth_dict[comment] = item['result']
    
    for item in predictions:
        # Ensure the predicted comment is a string
        predicted_comment = ' '.join(item['comment']) if isinstance(item['comment'], list) else item['comment']
        if predicted_comment in truth_dict:
            if truth_dict[predicted_comment] == item['result']:
                correct += 1
    
    accuracy = (correct / total) * 100 if total > 0 else 0
    return accuracy


def main():
    # Load data from files
    annotated_results = load_data(os.path.join(script_directory, "Annotated_Results.json"))
    bert_results = load_data(os.path.join(script_directory, "BERT_sentiment.json"))
    comment_sentiment_results = load_data(os.path.join(script_directory, "comment_sentiment_score.json"))
    
    # Calculate accuracy for BERT results
    bert_accuracy = calculate_accuracy(annotated_results, bert_results)
    print(f"BERT Model Accuracy: {bert_accuracy:.2f}%")
    
    # Calculate accuracy for Comment Sentiment Score results
    comment_sentiment_accuracy = calculate_accuracy(annotated_results, comment_sentiment_results)
    print(f"Comment Sentiment Score Model Accuracy: {comment_sentiment_accuracy:.2f}%")

if __name__ == "__main__":
    main()
