from pyrogram import Client, filters
from config import pref_p
import const
@Client.on_message(filters.command(["c","crash", "random"], prefixes=pref_p) & filters.me)
async def crasher(client, message):
    await message.edit_text(const.emcrash)
    await message.delete()