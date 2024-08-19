import os
from typing import List, Literal
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from w3lib.html import remove_tags
from youtube_transcript_api import YouTubeTranscriptApi

from ingest.models import (GithubRepo, HackerNewsStory, LobstersNewsStory,
                           SlashdotNewsStory)
from ingest.utils import get


def get_hn_story(story_id: int) -> HackerNewsStory:
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    res = get(url)
    if res.get("text"):
        res["text"] = remove_tags(res.get("text"))
    try:
        return HackerNewsStory(**res)
    except Exception as e:
        print(res, story_id, e, url)


def get_hn_stories(limit: int = 50) -> List[HackerNewsStory]:
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    res = []
    stories = get(url)[:limit]
    for story_id in stories:
        try:
            processed_story = get_hn_story(story_id)
            res.append(processed_story)
        except Exception:
            pass
    return res


def get_lobsters_stories() -> List[LobstersNewsStory]:
    data = []
    for num in range(1, 3):
        url = f"https://lobste.rs/page/{num}"

        res = httpx.get(url).text
        soup = BeautifulSoup(res, "html.parser")
        items = [
            LobstersNewsStory(
                title=item.find("span", class_="h-cite").text.strip(),
                url=item.find("a").get("href"),
            )
            for item in soup.findAll("div", class_="details")
        ]
        data.extend(items)
    return data


def get_slashdot_stories() -> List[SlashdotNewsStory]:
    url = "https://rss.slashdot.org/Slashdot/slashdotMain"
    res = httpx.get(url).text
    soup = BeautifulSoup(res, "xml")
    items = [
        SlashdotNewsStory(
            title=item.find("title").text.strip(),
            text=remove_tags(item.find("description").text.strip()).replace(
                "\n\n\n\n\n\nRead more of this story at Slashdot.", ""
            ),
            url=item.find("link").text,
        )
        for item in soup.find_all("item")
    ]

    return items


def get_trending_github_repos(
    spoken_language: str = "en",
    time_range: Literal["daily", "weekly", "monthly"] = "daily",
    language: str = None,
) -> List[GithubRepo]:
    base_url = "https://github.com/trending/"

    if language:
        base_url += language

    params = {
        "spoken_language_code": spoken_language.lower(),
        "since": time_range,
    }
    url = base_url + "?" + urlencode(params)
    res = httpx.get(url).text
    soup = BeautifulSoup(res, "html.parser")
    repos = soup.find_all("article")
    items = [
        GithubRepo(
            title="".join(item.find("a", class_="Link").text.split()),
            text=item.find("p", class_="col-9").text.strip(),
            url=f"https://github.com/{"".join(item.find("a", class_="Link").text.split())}",
        )
        for item in repos
    ]

    return items


def get_yt_video_transcript(video_id: str):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join(item.get("text").strip().replace("\n", " ") for item in transcript)
    return text


def get_yt_comments(video_id: str):
    # Replace with your own API key
    api_key = os.getenv("YOUTUBE_API_KEY")

    # Create a YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)

    # Retrieve comments
    def get_comments(youtube, video_id):
        comments = []
        results = (
            youtube.commentThreads()
            .list(
                part="snippet", videoId=video_id, textFormat="plainText", maxResults=100
            )
            .execute()
        )

        while results:
            for item in results["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            if "nextPageToken" in results:
                results = (
                    youtube.commentThreads()
                    .list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=100,
                        pageToken=results["nextPageToken"],
                    )
                    .execute()
                )
            else:
                break

        return comments

    # Get and print comments
    video_comments = get_comments(youtube, video_id)
    return video_comments


def get_reddit_posts(subreddit: str = None) -> List:
    if subreddit:
        url = f"https://www.reddit.com/r/{subreddit}.json"
    else:
        url = "https://www.reddit.com/r/popular.json"
        
    res = httpx.get(url)
    if res.status_code == 200:
        posts = res.json().get("data").get("children")
        data = [{
            "title": post.get("data", {}).get("title"),
            "link": post.get("data", {}).get("url_overridden_by_dest"),
            "text": post.get("data", {}).get("selftext")
            }
                for post in posts]
        return data
    return []
