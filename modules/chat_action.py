from pyrogram import Client, filters, enums
from config import pref_p
import asyncio
import random
import re
import json
actions = [enums.ChatAction.CANCEL, enums.ChatAction.CHOOSE_CONTACT, enums.ChatAction. CHOOSE_STICKER, enums.ChatAction.FIND_LOCATION, enums.ChatAction.IMPORT_HISTORY, enums.ChatAction.PLAYING, enums.ChatAction.RECORD_AUDIO, enums.ChatAction.RECORD_VIDEO, enums.ChatAction.RECORD_VIDEO_NOTE, enums.ChatAction.SPEAKING, enums.ChatAction.TYPING, enums.ChatAction.UPLOAD_AUDIO, enums.ChatAction.UPLOAD_DOCUMENT, enums.ChatAction.UPLOAD_PHOTO, enums.ChatAction.UPLOAD_VIDEO, enums.ChatAction.UPLOAD_VIDEO_NOTE]
@Client.on_message(filters.command(["action", "действие", "act"], prefixes=pref_p)& filters.me)
async def chat_action(client, message):
    match = re.search(r"\.(?:action|действие|act)\s+(.*)", message.text)
    if match == None:
        await message.edit_text(f"""Формат команды: \n `.act Чат.действие @usename`\nСписок действий - <blockquote>Отменить действие в чате - ca/cancel\nВыберает контакт - cc/ccontac\nВыберает стикер - cs/csticker\nИграет - p/play
Ищет геопозицию - geo/localtion\nЗагружает историю - ih/ihistory\nЗаписывает гс - ra/raudio/speak\nЗаписывает виде - rv/rvideo\nЗаписывает кружок - rc/rcircle\nПишет - t/typing\nГоворит в звонке - call/speakg
Загружает аудио - ua/uaudio\nЗагружает документ - ud/udocs\nЗагружает фото - up/uphoto\nЗагружает видео - uv/uvideo\nЗагружает кружок - uc/ucircle\nРандом - r</blockquote>""")
        return
    action = match.group(1)
    if action in ["h", 'help']:
        await message.edit_text(f"""Формат команды: \n `.act Чат.действие @usename`\nСписок действий - <blockquote>Отменить действие в чате - ca/cancel\nВыберает контакт - cc/ccontac\nВыберает стикер - cs/csticker\nИграет - p/play
Ищет геопозицию - geo/localtion\nЗагружает историю - ih/ihistory\nЗаписывает гс - ra/raudio/speak\nЗаписывает виде - rv/rvideo\nЗаписывает кружок - rc/rcircle\nПишет - t/typing\nГоворит в звонке - call/speakg
Загружает аудио - ua/uaudio\nЗагружает документ - ud/udocs\nЗагружает фото - up/uphoto\nЗагружает видео - uv/uvideo\nЗагружает кружок - uc/ucircle\nРандом - r</blockquote>""")
        return
    user_id = str((await client.get_me()).id)
    if len(action.split()) > 1:
        tag, action = action.split()[1], action.split()[0]
    else:
        tag = None
    if tag == None:
        chat_id = message.chat.id
    else:
        chat_id = tag
    print(chat_id)
    if action in ["ca", "cancel"]:
        await message.delete()
        action_c = await handler_act(action)
        with open('users.json', 'r') as f:
            data = json.load(f)
            stop_action = data[user_id]['stop_action'] = True
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)
        return
    action_c = await handler_act(action)
    await message.delete()
    with open('users.json', 'r') as f:
            data = json.load(f)
            stop_action = data[user_id]['stop_action'] = False
    with open('users.json', 'w') as f:
        json.dump(data, f, indent=2)
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
            stop_action = data[user_id]['stop_action']
        if stop_action == False:
            await client.send_chat_action(chat_id, action_c)
            await asyncio.sleep(6)
            action_c = await handler_act(action)
        else:
            break
    
async def handler_act(action):
    if action in ["ca", "cancel"]:
        return actions[0]
    elif action in ["cc", "ccontact"]:
        return actions[1]
    elif action in ["cs", "csticker"]:
        return actions[2]
    elif action in ["p", "play"]:
        return actions[3]
    elif action in ["geo", "location"]:
        return actions[4]
    elif action in ["ih", "ihistory"]:
        return actions[5]
    elif action in ["ra", "raudio", "speak"]:
        return actions[6]
    elif action in ["rv", "rvideo"]:
        return actions[7]
    elif action in ["rc", "rcircle"]:
        return actions[8] 
    elif action in ["call", "speakg"]:
        return actions[9]
    elif action in ["t", "typing"]:
        return actions[10]
    elif action in ["ua", "uaudio"]:
        return actions[11]
    elif action in ["ud", "udocs"]:
        return actions[12]
    elif action in ["up", "uphoto"]:
        return actions[13]
    elif action in ["uv", "uvideo"]:
        return actions[14]
    elif action in ["uc", "ucircle"]:
        return actions[15]
    elif action in ["r", "random"]:
        return random.choice(actions)