from pyrogram import Client, filters
from config import pref_p

@Client.on_message(filters.command(["games", "игры", "game"], prefixes=pref_p)& filters.me)
async def games(client, message):
    text = """<emoji id=5467583879948803288>🎮</emoji>Игры которые поддерживает бот:
<blockquote><emoji id=5429503304038106656>🪙</emoji> [Blum](https://t.me/BlumCryptoBot)
⛏ [Zavod](https://t.me/Mdaowalletbot)\n🦁 [TabiZoo](https://t.me/tabizoobot)
<emoji id=5328290660246101415>🏎</emoji> [OKX Racer](https://t.me/OKX_official_bot)
<emoji id=5967646230732347419>🐹</emoji> [Hamster Combat](https://t.me/hamster_kombat_bot)
<emoji id=5231394776414178774>🎩</emoji> [X-Empire](https://t.me/muskempire_bot)
<emoji id=5276424673834317384>🚀</emoji> [PocketFi](https://t.me/pocketfi_bot)
🥶 [Iceberg](https://t.me/IcebergAppBot)
<emoji id=5363919733248773777>📦</emoji> [Cubes](https://t.me/cubesonthewater_bot)
<emoji id=5816707898696274976>⭐️</emoji> [Major](https://t.me/starmajorbot)
<emoji id=5453918011272470772>🏎</emoji> [Race](https://t.me/Racememe_bot)
<emoji id=5426931877053222753>🌐</emoji> [Vertus](https://t.me/seed_coin_bot)
<emoji id=5449885771420934013>🌱</emoji> [Seed](https://t.me/seed_coin_bot)
<emoji id=5451732530048802485>⏳</emoji>[Time Farm](https://t.me/TimeFarmCryptoBot)
<emoji id=5267237618529088267>👊</emoji>[Dogiators](https://t.me/Dogiators_bot)
<emoji id=5258113810912267471>😉</emoji>[Ton Station](https://t.me/tonstationgames_bot) </blockquote>"""
    await message.edit_text(text) 