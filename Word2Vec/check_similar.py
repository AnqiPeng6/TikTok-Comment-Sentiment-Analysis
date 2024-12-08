from TikTokApi import TikTokApi
import asyncio
import os
from gensim.models import Word2Vec
from word2vec import update_word2vec_model, update_trending_comments, load_word2vec_model
from TikTokApi.TrendingComments.get_comments import get_comments, get_comments_for_videos
from TikTokApi.TrendingComments.get_trending_videos import trending_videos
os.chmod('/Users/anqi/TikTok-Api/word2vec/word2vec.model', 0o666)  # Grants read/write permissions

def print_similar_words(word, word2vec_model):
    """
    Print the most similar words to the given word from the Word2Vec model.

    Args:
        word (str): The word to find similar words for.
        word2vec_model: The trained Word2Vec model.
    """
    if word in word2vec_model.wv.key_to_index:
        similar_words = word2vec_model.wv.most_similar(word, topn=25)
        print(f"Most similar words to '{word}':")
        for similar_word, similarity in similar_words:
            print(f"{similar_word}: {similarity:.2f}")
    else:
        print(f"'{word}' not found in vocabulary.")


if __name__ == "__main__":

    word2vec_model = load_word2vec_model()
    print_similar_words("sounds", word2vec_model)
    print("Number of words in the model:", len(word2vec_model.wv))

    # Check if the word 'pretty' is in the vocabulary
