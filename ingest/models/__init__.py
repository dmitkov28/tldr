from typing import Optional
from pydantic import BaseModel


class HackerNewsStory(BaseModel):
    title: Optional[str]
    url: Optional[str] = None
    text: Optional[str] = None


class LobstersNewsStory(BaseModel):
    title: Optional[str]
    url: Optional[str]
