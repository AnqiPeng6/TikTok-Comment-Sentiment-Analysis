from TikTokApi import TikTokApi
import asyncio
import os
from gensim.models import Word2Vec
from TikTokApi.api.video import Video

# Define video ID and ms_token

ms_token = os.environ.get("ms_token", None)  # Set your own ms_token

# Function to scrape TikTok comments
async def get_comments(video_id, total_comments=1000):
    """
    Scrape TikTok comments for a given video ID.

    Args:
        video_id (str): The ID of the TikTok video.
        total_comments (int): The total number of comments to retrieve.

    Returns:
        list of str: A list containing the text of the comments.
    """
    comments_list = []  # Local list to hold the comments
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(id=video_id)

        count = 0
        cursor = 0  # Initial cursor to start fetching comments from the beginning
        
        # Fetch comments in a loop until you get enough
        #while true:
        
       
        #comment_count = await video.get_comment_count()
    
        # Access the comment count from the video's stats
        #comment_count = video_info.get("stats", {}).get("commentCount", 0)
        #comment_count = await video.get_comment_count()
        
        async for comment in video.comments(count = total_comments):
            comments_list.append(comment.text)
            count += 1

            # If there are no more comments to fetch, break the loop
            #if len(comments_list) >= total_comments:
                #break
            
            

    
    
    return [comment.split() for comment in comments_list]  # Return the list of comments




async def get_comments_for_videos(video_ids, total_comments=100):
    """
    Scrape TikTok comments for a list of video IDs.

    Args:
        video_ids (list of str): A list of TikTok video IDs.
        total_comments (int): The total number of comments to retrieve per video.

    Returns:
        list of str: A single list containing the text of all comments from all videos.
    """
    all_comments = []  # Single list to hold comments from all videos
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        
        for video_id in video_ids:
            video = api.video(id=video_id)
            count = 0

            async for comment in video.comments(count=30):
                all_comments.append(comment.text)
                

                

    return [comment.split() for comment in all_comments]



            
async def get_hashtag_videos(count = 10):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        tag = api.hashtag(name="funny")
        async for video in tag.videos(count):
            return video
        
async def get_related_videos(URL = "https://www.tiktok.com/@davidteathercodes/video/7074717081563942186"):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(
            url=URL
        )

        async for related_video in video.related_videos(count=10):
            print(related_video)
            print(related_video.as_dict)

        video_info = await video.info()  # is HTML request, so avoid using this too much
        print(video_info)
        video_bytes = await video.bytes()
        with open("video.mp4", "wb") as f:
            f.write(video_bytes)
            
async def get_video_from_user(User = "therock"):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user(User)
        user_data = await user.info()
        print(user_data)

        async for video in user.videos(count=30):
            print(video)
            print(video.as_dict)

        async for playlist in user.playlists():
            print(playlist)
            
            
async def sound_videos(sound_id = "7016547803243022337"):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        async for sound in api.sound(id=sound_id).videos(count=30):
            print(sound)
            print(sound.as_dict)