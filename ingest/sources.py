from typing import List

import httpx
from ingest.models import HackerNewsStory, LobstersNewsStory
from ingest.utils import get
from w3lib.html import remove_tags
from bs4 import BeautifulSoup


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


def get_lobsters_data() -> List[LobstersNewsStory]:
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
