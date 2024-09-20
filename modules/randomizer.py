from pyrogram import Client, filters
from config import pref_p
import random
import re
@Client.on_message(filters.command(["rnd","рнд", "random"], prefixes=pref_p) & filters.me)
async def ran1(client, message):
    match = re.search(r"\.(?:rnd|random|рандом)\s+(.*)", message.text)
    mrnd = match.group(1)
    print(mrnd)
    rnd = random.randint(1, int(mrnd))
    await message.edit_text(f"<emoji id=5226478073947371707>🎲</emoji> Рандомное число - {rnd}")

#Bad code|Плохой код
@Client.on_message(filters.command(["try","трай"], prefixes=pref_p) & filters.me)
async def try_(client, message):
    match = re.search(r"\.(?:try|трай)\s+(.*)", message.text)
    text = match.group(1)
    rnd = random.randint(1, 2)
    if rnd == 1:
        await message.edit_text(f"{text} - Удачно")
    else:
        await message.edit_text(f"{text} - Неудачно")
