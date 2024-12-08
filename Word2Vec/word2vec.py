from TikTokApi import TikTokApi
import asyncio
import os
import sys
from gensim.models import Word2Vec
# Add the word2vec directory to sys.path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from TikTokApi.TrendingComments.get_trending_videos import trending_videos, get_hashtag_videos

os.chmod('/Users/anqi/TikTok-Api/word2vec/word2vec.model', 0o666)  # Grants read/write permissions

model_path = '/Users/anqi/TikTok-Api/word2vec/word2vec.model'


def update_word2vec_model(word2vec_model, tokenized_comments):
    """
    Update the existing Word2Vec model with new tokenized comments.

    Args:
        word2vec_model (Word2Vec): The existing Word2Vec model to be updated.
        tokenized_comments (list of list of str): New tokenized comments for training.

    Returns:
        None
    """
    # Build vocabulary from new comments, updating the existing model
    word2vec_model.build_vocab(tokenized_comments, update=True)

    # Train the model with the new comments
    word2vec_model.train(tokenized_comments, total_examples=len(tokenized_comments), epochs=word2vec_model.epochs)

    # Optionally, save the updated model
    word2vec_model.save("/Users/anqi/TikTok-Api/Word2Vec/word2vec.model")


async def update_trending_comments():
    from TikTokApi.TrendingComments.get_comments import get_comments_for_videos
    video_ids = await trending_videos()
    
    all_comments = await get_comments_for_videos(video_ids)
    model = load_word2vec_model()
    update_word2vec_model(model, all_comments)
    
    
async def update_hashtag_comments():
    from TikTokApi.TrendingComments.get_comments import get_comments_for_videos
    video_ids = await get_hashtag_videos()
    
    all_comments = await get_comments_for_videos(video_ids)
    model = load_word2vec_model()
    update_word2vec_model(model, all_comments)

def load_word2vec_model():
    model = Word2Vec.load(model_path)
    return model
    
    
if __name__ == "__main__":
   
        # Run the main coroutine inside asyncio.run
    model = load_word2vec_model()
    print(model.epochs)
  