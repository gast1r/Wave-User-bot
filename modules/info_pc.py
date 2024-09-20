from pyrogram import Client, filters
from config import pref_p
import psutil
import speedtest
import platform
@Client.on_message(filters.command(["инфо","info"], prefixes=pref_p) & filters.me)
async def info(client, message):
 cpu_count = psutil.cpu_count()
 version = platform.version() 
 g = psutil.virtual_memory()
 await message.edit_text(f"**<emoji id=5172494668658639634>💻</emoji> Данные о сервере: \n<emoji id=5172869086727635492>💻</emoji>CPU: {cpu_count} \n<emoji id=5174693704799093859>💻</emoji> RAM: {round(g.total / 1024 / 1024 )} / {round(g.used / 1024 / 1024 )} MB ({g.percent}%) \n\n<emoji id=5172881503478088537>💻</emoji>ARCH: x64 \n<emoji id=5300985968302498775>👩‍💻</emoji>OS: {version}**")