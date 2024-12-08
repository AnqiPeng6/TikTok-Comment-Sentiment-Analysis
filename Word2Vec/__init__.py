from .word2vec import (
    update_word2vec_model,
    update_trending_comments,
    update_hashtag_comments,
    load_word2vec_model
)

# Optional: Define a list of functions/classes to expose
__all__ = [
    "update_word2vec_model",
    "update_trending_comments",
    "update_hashtag_comments",
    "load_word2vec_model",
]