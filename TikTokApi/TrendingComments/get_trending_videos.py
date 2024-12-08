from TikTokApi import TikTokApi
import asyncio
import os

ms_token = os.environ.get("ms_token", None)  # set your own ms_token


async def trending_videos():
    video_ids = []
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        async for video in api.trending.videos(count=30):
            video_ids.append(video.id)  # Extract the video ID and append it to the list

    return video_ids  # Return the list of video IDs

async def get_hashtag_videos():
    video_ids = []
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        tag = api.hashtag(name="funny")
        async for video in tag.videos(count=30):
            video_ids.append(video.id)
    return video_ids

