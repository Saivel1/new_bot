from urllib.parse import unquote
from marzban.backend import MARZ_DATA, BackendContext
from logger_setup import logger

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

async def get_links(links: list):
    response = []
    for link in links:
        sta = link.find("#")
        encoded = link[sta+1:]
        text = unquote(encoded)
        response.append(text)
    return response