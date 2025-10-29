from urllib.parse import unquote
from marzban.backend import MARZ_DATA, BackendContext

ctx = BackendContext(*MARZ_DATA)

prices = [
    ("50 рублей", '50_r'),
    ("150 рублей", '150_r'),
    ("300 рублей", '300_r'),
    ("600 рублей", '600_r')
]

sub_servs = [
    ("Main", "main")
]


platforms = [
    ("Adriod", 'android'),
    ("IOS | MacOS", 'ios'),
    ("Windows", 'windows')
]

async def get_links(username):
    username = str(username)
    async with ctx as backend:
        res = await backend.get_user(username)
        marz_links = res.get("links") #type: ignore

        response = []
        for link in marz_links:
            sta = link.find("spx=#")
            encoded = link[sta+5:]
            text = unquote(encoded)
            response.append(
                (text, link)
            )
        return response