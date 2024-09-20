from pyrogram import Client, filters
from config import pref_p
import random
import const

@Client.on_message(filters.command(["цитата", "стетхем"], prefixes=pref_p) & filters.me)
async def quote(client, message):
    rnd = random.randint(1, 17)
    await message.edit_text(f"{const.quote[rnd]}\n©Джейсон Стетхем")
