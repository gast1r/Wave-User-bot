from pyrogram import Client, filters
from config import pref_p, version

@Client.on_message(filters.command(["help", "помощь","команды"], prefixes=pref_p)& filters.me)
async def help(client, message):
    await message.edit_text("<emoji id=5436113877181941026>❓</emoji> Список команд: https://teletype.in/@wave_userbot/commands \n<emoji id=5188468322047371084>🏖️</emoji> WaveBot - @Wave_userbot \n<emoji id=5447410659077661506>🌐</emoji> Version:" + version)