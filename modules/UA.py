from pyrogram import Client, filters
from config import pref_p
import re
from utils.agents import get_UA, generate_random_user_agent
import json
@Client.on_message(filters.command(["UA","юзер агент", "user agent"], prefixes=pref_p) & filters.me)
async def UA(client, message):
    user_id = str((await client.get_me()).id)
    match = re.search(r"\.(?:ua|юзер агент|user agent)\s+(.*)", message.text)
    if match == None:
        ua = get_UA(user_id)
        await message.edit_text(f"<emoji id=5282843764451195532>🖥</emoji>Твой UA: {ua} \n\n<emoji id=5472146462362048818>💡</emoji> Также вы можете поменять на свой, переходим по [ссылке](https://clck.ru/3CCW8N), копируем UA, пишем .ua <UA> (желательно мобильный)")
        return
    ua = match.group(1)
    if ua == "r":
        with open('users.json', 'r') as f:
            data = json.load(f)
            ua = data[user_id]['UA'] = generate_random_user_agent()
        with open('users.json', 'w') as f:
                    json.dump(data, f, indent=2)
        await message.edit_text(f"Успешно поменяли UA!\nТвой UA: {ua}")
        return 
    else:
        await message.edit_text(f"Успешно поменяли UA!\nТвой UA: {ua}")




