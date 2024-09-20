from pyrogram import Client, filters, types
from config import pref_p
import re


@Client.on_message(filters.command("eval", prefixes=pref_p) & filters.me)
async def getchat(app, message):
    match = re.search(r"\.(?:погода|weather)\s+(.*)", message.text)
    pla = match.group(1)
    print(eval(pla))
    answer = eval(pla)
    await message.edit_text(f"Ваш пример - {pla}={answer}")
