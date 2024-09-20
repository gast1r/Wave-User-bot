import requests
from pyrogram import Client, filters
import asyncio
from config import pref_p

def get_creation_date(id: int) -> str:
    url = "https://restore-access.indream.app/regdate"
    headers = {
        "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128"
    }
    data = {"telegramId": id}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["data"]["date"]
    else:
        return "Ошибка получения данных"
    
@Client.on_message(filters.command(["accdate", "аккдата"], prefixes=pref_p)& filters.me)
async def dateacc(client, message):
    try:
        if message.reply_to_message is None:
            user_id = str((await client.get_me()).id)
        else:
            user_id = message.reply_to_message.from_user.id
        date = get_creation_date(id=user_id)
        await message.edit_text(f"🕰 Дата регистрации этого аккаунта: {date}")
    except:
        await asyncio.sleep(3)