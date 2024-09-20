from pyrogram import Client, filters
from config import pref_p, id_admin
import subprocess
import re
import json
import asyncio, os
from modules.settings import checker
from promo_key.games import games
@Client.on_message(filters.command(["term","терм"], prefixes=pref_p) & filters.me)
async def term(client, message):
     user_id = str((await client.get_me()).id)
     if str(user_id) == id_admin:
         command = message.text.replace(".term ", "")
         try:
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = process.stdout.strip()  
            error = process.stderr.strip() 
            if output:
                await message.edit_text(f"**Output:**{output}")
            if error:
                await message.edit_text(f"**Error:**{error}")
         except Exception as e:
            await message.edit_text(f"**Error:**{e}")
     else:
         pass
@Client.on_message(filters.command(["restart","рестарт"], prefixes=pref_p) & filters.me)
async def rest(client, message):
     user_id = str((await client.get_me()).id)
     if str(user_id) == id_admin:
         try:
            await message.edit_text(f"**Перезагружаю бота...**")
            await message.delete()
            process = subprocess.run('pm2 restart main', shell=True, capture_output=True, text=True)
             # Выводим результат в сообщение
            output = process.stdout.strip()  # Убираем лишние пробелы
            error = process.stderr.strip()  # Убираем лишние пробелы
         except Exception as e:
            await message.edit_text(f"**Error:**{e}")
     else:
         pass



@Client.on_message(filters.command(["fixgb", ], prefixes=pref_p) & filters.me)
async def ffblumwe(client, message):
     user_id = str((await client.get_me()).id)
     if str(user_id) == id_admin:
         with open('global.json', 'r') as f:
            data = json.load(f)
            text = data['game_started']
         if text == True:
             data['game_started'] = False
             with open('global.json', 'w') as f:
                    json.dump(data, f, indent=2)
             await message.edit_text(f"Исправил")
         else:
             await message.edit_text(f"Все норм")
     else:
         await message.edit_text(f"Нет доступа!")
         await asyncio.sleep(2)
         await message.delete()


@Client.on_message(filters.command(["msg"], prefixes=pref_p) & filters.me)
async def msgid(client, message):
     user_id = str((await client.get_me()).id)
     if str(user_id) == id_admin:
         print(message.reply_to_message.reply_markup.inline_keyboard)
     else:
         await message.edit_text(f"Нет доступа!")
         await asyncio.sleep(2)
         await message.delete()


@Client.on_message(filters.command(["json", "db", "бд"], prefixes=pref_p) & filters.me)
async def jsonbd(client, message):
     user_id = str((await client.get_me()).id)
     if str(user_id) == id_admin:
         await message.delete()
         await client.send_document("me", "users.json", caption="database")
     else:
         await message.edit_text(f"Нет доступа!")
         await asyncio.sleep(2)
         await message.delete()

  
@Client.on_message(filters.command(["logs", "логи"], prefixes=pref_p) & filters.me)
async def logstxt(client, message):
     user_id = str((await client.get_me()).id)
     if str(user_id) == id_admin:
         await message.delete()
         await client.send_document("me", "logs_auto.txt", caption="logs")
     else:
         await message.edit_text(f"Нет доступа!")
         await asyncio.sleep(2)
         await message.delete()


@Client.on_message(filters.command(["gamechange", "смигру", "gchange"], prefixes=pref_p) & filters.me)
async def game_changer(client, message):
     user_id = str((await client.get_me()).id)
     if str(user_id) == id_admin:
        match = re.search(r"\.(?:gamechange|смигру|gchange)\s+(.*)", message.text)
        game = match.group(1)
        print(game)
        with open(f"cfg.txt", "w", encoding="utf-8") as text_file:
         text_file.write(f"{game}")

        await message.delete()
        process = subprocess.run('pm2 restart HGK', shell=True, capture_output=True, text=True)
     else:
         await message.edit_text(f"Нет доступа!")
         await asyncio.sleep(2)
         await message.delete()


@Client.on_message(filters.command(["iхамстер", "ihamster", "iham"], prefixes=pref_p) & filters.me)
async def info_hamster(client, message):
    promo_counts = {}
    for game in games:
        keys_file = game["keys_file"]
        if os.path.exists(keys_file):
            with open(keys_file, 'r') as file:
                lines = file.readlines()
                promo_counts[game["name"]] = len(lines)
        else:
            print(f"Файл с ключами {keys_file} не найден.")
    text = "🔑 Всего промокодов:\n"
    for game_name, count in promo_counts.items():
        text += f" {game_name} - {count}\n"

    await message.edit_text(text)
@Client.on_message(filters.command(["settapp","asett", "sappp"], prefixes=".") & filters.me)
async def settings(client, message):
    user_id = str((await client.get_me()).id)
    if str(user_id) == id_admin:
     with open('users.json', 'r') as f:
          data = json.load(f)
     user = await client.resolve_peer(message.command[1].replace('@', ''))
     user_id = str(user.user_id)
     text = ""
     for app in data[user_id].keys():
        if app.startswith("auto_"):
             text += checker(app, user_id, data)
     await message.edit_text(f"<emoji id=5372981976804366741>🤖</emoji> Автомизация:\n<blockquote>{text}</blockquote>")
    else:
         await message.edit_text(f"Нет доступа!")
         await asyncio.sleep(2)
         await message.delete()

@Client.on_message(filters.command(["logs", "логи"], prefixes=pref_p) & filters.me)
async def combosend(client, message):
     user_id = str((await client.get_me()).id)
     if str(user_id) == id_admin:
         await message.delete()
         await client.send_document("me", "combo.json", caption="logs")
     else:
         await message.edit_text(f"Нет доступа!")
         await asyncio.sleep(2)
         await message.delete()
