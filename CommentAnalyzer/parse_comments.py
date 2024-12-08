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

# Global variable for processed comments
processed_comments = []

# Function to load processed comments from a file
def load_processed_comments():
    global processed_comments
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the processed_comments.json file
    file_path = os.path.join(script_directory, "processed_comments.json")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            processed_comments = json.load(file)
    except FileNotFoundError:
        processed_comments = []

# Function to save processed comments to a file
def save_processed_comments():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the processed_comments.json file
    file_path = os.path.join(script_directory, "processed_comments.json")
    word2vec = load_word2vec_model()
    update_word2vec_model(word2vec, processed_comments)
    with open(file_path, "r", encoding="utf-8") as file:
        json.dump(processed_comments, file, ensure_ascii=False, indent=4)

# Function to print processed comments
def print_processed_comments():
    global processed_comments
    load_processed_comments()  # Load comments from the file
    print("Processed Comments:")
    print("=" * 50)
    for comment in processed_comments:
        print(" ".join(comment))  # Join the split words back into a readable sentence
    print("=" * 50)

# Initialize sentiment analysis pipeline using BERT
sentiment_analysis = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

ms_token = os.environ.get("ms_token", None)  # set your own ms_token

async def get_hashtag_videos():
    video_ids = []  # To store video IDs
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        tag = api.hashtag(name="meme")
        async for video in tag.videos(count=30):
            print(video)
            print(video.as_dict)
            video_ids.append(video.id)  # Store video ID
    return video_ids  # Return list of video IDs

async def get_comments_and_analyze(video_ids):
    global processed_comments
    comments_list = []  # Local list to hold the comments

    # Open a file for writing comments and sentiment results
    with open("BERT_sentiment.txt", "w", encoding="utf-8") as file:
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
            
            for video_id in video_ids:  # Loop through each video ID
                file.write(f"Video ID: {video_id}\n")
                file.write("=" * 50 + "\n")
                
                video = api.video(id=video_id)
                count = 0
                async for comment in video.comments(count=30):
                    comments_list.append(comment.text)
                    comment_text = comment.as_dict.get('text', '')  # Get comment text
                    if comment_text:
                        # Perform sentiment analysis
                        result = sentiment_analysis(comment_text)[0]
                        sentiment = result['label']
                        score = result['score']
                        
                        # Write comment and sentiment to file
                        file.write(f"Comment: {comment_text}\n")
                        file.write(f"Sentiment: {sentiment}, Score: {score}\n")
                        file.write("-" * 50 + "\n")
                    
                    count += 1
                    if count >= 30:  # Limit to 30 comments per video
                        break
                
                processed_comments = [comment.split() for comment in comments_list]  # Process comments
                save_processed_comments()  # Save processed comments to the file
                file.write("\n")

async def main():
    # Step 1: Get video IDs
    # video_ids = await get_hashtag_videos()
    
    # print("Fetched video IDs:")
    # for video_id in video_ids:
    #     print(video_id)

    # # Step 2: Fetch comments and analyze sentiment
    # await get_comments_and_analyze(video_ids)
    load_processed_comments()
    comments = processed_comments
    results = []
    for comment in comments:
        # Perform sentiment analysis
        analysis = sentiment_analysis(comment)[0]

        # Extract the digit from the label if present, otherwise handle the exception
        try:
            # Extracting the last character and assuming it's a digit
            score = int(analysis['label'][0])
        except ValueError:
            # Handle cases where conversion fails
            print(f"Error converting label {analysis['label']} to score.")
            continue  # Skip this entry or handle differently based on your needs

        # Determine sentiment category based on the score
        if score < 3:
            sentiment = 'negative'
        elif score > 3:
            sentiment = 'positive'
        else:
            sentiment = 'neutral'

        # Append the result with the score and sentiment category included
        results.append({
            "comment": comment,
            "result": sentiment,
            "score": score
        })


# Save the results to a JSON file
    with open('BERT_sentiment.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Uncomment to run the async main function
    asyncio.run(main())

    # Print the processed comments
    #print_processed_comments()
