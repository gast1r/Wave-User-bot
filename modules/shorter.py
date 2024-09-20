from pyrogram import Client, filters
from config import pref_p
import pyshorteners
@Client.on_message(filters.command(["shorter", "сократи"], prefixes=pref_p)& filters.me)
async def sokr(app, message):
    try:
        url = message.command[1]
    except:
        await message.edit_text("❌ Ошибка")
    surl = pyshorteners.Shortener().clckru.short(url)
    await message.delete()
    await app.send_message(message.chat.id,f"<emoji id=5373105190826167242>🧐</emoji> Сокращенная [ссылка]({surl}) ")
