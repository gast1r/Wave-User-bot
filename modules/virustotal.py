from pyrogram import Client, filters
from config import pref_p


@Client.on_message(filters.command(["virustotal", "действие", "act"], prefixes=pref_p)& filters.me)
async def chat_action(client, message):
    print('f')