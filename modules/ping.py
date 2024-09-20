from pyrogram import Client, filters
from config import pref_p
from time import perf_counter
import datetime 
@Client.on_message(filters.command(["ping","пинг"], prefixes=pref_p) & filters.me)
async def ping(client, message):
    start = perf_counter()
    await message.edit_text("<emoji id=5021905410089550576>✅</emoji> Понг!\n")
    finish = perf_counter()
    ago_time = round(finish - start, 3)
    await message.edit_text(f"**<emoji id=5021905410089550576>✅</emoji> Понг!\n {ago_time} секунд**")