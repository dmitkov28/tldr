import httpx
import re


def get(url: str):
    res = httpx.get(url)
    if res.status_code == 200:
        return res.json()


def get_youtube_video_id_from_url(video_url: str) -> str:
    pattern = r"v=([^&]+)"
    match = re.search(pattern, video_url)
    if match:
        video_id = match.group(1)
    return video_id
