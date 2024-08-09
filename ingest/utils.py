import httpx


def get(url: str):
    res = httpx.get(url)
    if res.status_code == 200:
        return res.json()
