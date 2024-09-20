from pyrogram import Client, filters
from config import pref_p
import re
@Client.on_message(filters.command(["поиск", "search"], prefixes=pref_p)& filters.me)
async def search(app, message):
        match = re.search(r"\.(?:поиск|search)\s+(.*)", message.text)
        search = match.group(1)
        req = search
        # serch = message.command[1]
        search = search.replace(" ", "+")
        wurl = f"https://ru.m.wikipedia.org/wiki/{search}"
        yurl = f"https://ya.ru/search/?text={search}"
        url = f"https://www.google.com/search?q={search}"
        await message.edit_text(f"<emoji id=5188311512791393083>🔎</emoji> Вот что мне удалось найти по вашему запросу - **{req}**\n <emoji id= 5366254185413103773>👩‍💻</emoji> [Google]({url}) \n <emoji id=5373292717688245867>🤩</emoji> [Wiki]({wurl})\n <emoji id=5373105190826167242>🤩</emoji> [yandex]({yurl})")