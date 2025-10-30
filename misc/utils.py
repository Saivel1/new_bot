from urllib.parse import unquote
from dataclasses import dataclass
from repositories.base import BaseRepository
from db.database import async_session
from db.db_models import UserOrm
from marzban.backend import BackendContext
from datetime import datetime
from marzban.backend import MARZ_DATA, BackendContext
from misc.bot_setup import add_monthes
from datetime import timedelta

MONTH = 30

@dataclass(slots=True)
class LinksSub:
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


async def get_user(user_id):
    user_id = str(user_id)
    async with async_session() as session:
        user_repo = BaseRepository(session=session, model=UserOrm)
        res = await user_repo.get_one(user_id=user_id)
        return res
    

async def modify_user(username, expire: datetime):
    data = datetime.timestamp(expire)
    data = int(data)
    username = str(username)


    async with BackendContext(*MARZ_DATA) as backend:
        user = await backend.get_user(id=username)
        if not user:
            await backend.create_user(username=username)

        await backend.modify_user(
            id=username, 
            expire=data
        )


def new_date(expire: datetime, amount: str):
    amount = amount.split(".")[0]
    amou = int(amount)
    cnt_monthes = add_monthes.get(amou)
    
    return expire + timedelta(days=cnt_monthes*MONTH) #type: ignore


def calculate_expire(old_expire):
    current_time = datetime.now()
    
    if old_expire is None:
        new_expire = current_time
    elif old_expire >= current_time:
        new_expire = old_expire
    else:
        new_expire = current_time
    
    return new_expire