from pydantic import BaseModel
from urllib.parse import unquote
from dataclasses import dataclass

@dataclass(slots=True)
class LinksSub(BaseModel):
    sub_link: str
    links: list
    titles: list


async def to_link(lst_data: dict):
    links = lst_data.get("links")
    if links is None:
        return False
    
    titles = []
    for link in links:
        sta = link.find("#")
        encoded = link[sta+1:]
        text = unquote(encoded)
        titles.append(text)
    
    sub_link = lst_data.get('subscription_url')
    if sub_link is None:
        return None

    return LinksSub(
        sub_link=sub_link,
        links=links,
        titles=titles
    )