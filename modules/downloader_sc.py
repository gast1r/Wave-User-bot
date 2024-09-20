from pyrogram import Client, filters
from config import pref_p
from tiktok_downloader import snaptik
import tempfile
import os
import asyncio
@Client.on_message(filters.command("ttdll", prefixes=pref_p) & filters.me)
async def tt(client, message):
    try:
        link = message.command[1]   
    except:
        await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Укажите ссылку на видео TikTok")
        await asyncio.sleep(3)
        await message.delete()
        return
    get_video = snaptik(f"{link}")
    get_video_list = list(get_video)
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        get_video_list[0].download(temp_file.name)
        temp_file_path = temp_file.name
    with open(temp_file_path, "rb") as video:
        await message.delete()
        await client.send_video(message.chat.id, video, caption="<emoji id=5280662183057825163>🎥</emoji> Ваше видео с TikTok")
        os.remove(temp_file_path)