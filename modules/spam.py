from pyrogram import Client, filters
from config import pref_p
import asyncio
import json


@Client.on_message(filters.command(["spam", "спам"], prefixes=pref_p) & filters.me)
async def spam(client, message):
    user_id = str((await client.get_me()).id)
    await message.delete()
    times = message.command[1]
    time = message.command[2]
    to_spam = " ".join(message.command[3:])
    if int(times) <= 1000:
        if 0.05 <= float(time) <= 86400:
            with open('users.json', 'r') as f:
                data = json.load(f)
                spamstop = data[user_id]['spam_stop'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            for _ in range(int(times)):
                with open('users.json', 'r') as f:
                    data = json.load(f)
                    spamstop = data[user_id]['spam_stop']
                if spamstop:
                    print('stop')
                    break
                else:
                    await client.send_message(message.chat.id, to_spam)
                    await asyncio.sleep(float(time))
        else:
            await client.send_message(message.chat.id, "❌ Ошибка. Не меньше 0.20 и не больше 86400 секунд между отправкой сообщениями.")
            return
    else:
        await client.send_message(message.chat.id, "❌ Ошибка.Не больше 300 сообщений.")
        return
    
@Client.on_message(filters.command(["sspam", "сспам"], prefixes=pref_p) & filters.me)
async def stop_spam(client, message):
    user_id = str((await client.get_me()).id)
    with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['spam_stop'] = True
    with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)
    await message.edit_text(f"⛔️ Спам остановлен")