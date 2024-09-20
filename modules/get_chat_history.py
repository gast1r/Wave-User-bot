from pyrogram import Client, filters, types
from config import pref_p
import asyncio


@Client.on_message(filters.command("id", prefixes=pref_p) & filters.me)
async def peer(client, message):
 tag = message.text.split(" ", 1)[1]  # Получаем тег из сообщения
 peer = await client.resolve_peer(tag)
 id = peer.user_id
 text = f"🆔 ID чата {tag}: {id}"
 await message.edit_text(text)


@Client.on_message(filters.command("gh", prefixes=pref_p) & filters.me)
async def getchat(app, message):
    if len(message.command) < 4:
        chat_id = chech_int(message.command[2])
        my = chech_int(message.command[1])
        chat_id = message.command[2]
        msg = 0
    try:
        my = int(message.command[1])
        chat_id = int(message.command[2])
        msg = int(message.command[3])
    except:
        my = message.command[1]
        chat_id = message.command[2]
        msg = int(message.command[3])
    print(my, chat_id)
    print(msg)
    #my = -1002206343477  # ID вашего чата
    #chat_id = -1002002085211  # ID чата, из которого нужно пересылать

    async for message in app.get_chat_history(chat_id):
        await asyncio.sleep(0.001)
        if msg == 0:
            if message.text == None:
                text = ""
            else:
                text = message.text
            if message.video:
                video = await app.download_media(message, in_memory=True)
                await app.send_video(chat_id=my, video=video, caption=f"{text}")
            elif message.photo:
                photo = await app.download_media(message, in_memory=True)
                await app.send_photo(chat_id=my, photo=photo, caption=f"{text}")
            elif message.text:
                await app.send_message(my, message.text)
            else:
                pass
        elif message.id == msg:
            if message.video:
                video = await app.download_media(message, in_memory=True)
                await app.send_video(chat_id=my, video=video, caption=f"{message.text}")
                return
            elif message.photo:
                photo = await app.download_media(message, in_memory=True)
                await app.send_photo(chat_id=my, photo=photo, caption=f"{message.text}")
                return
            elif message.text:
                await app.send_message(my, message.text)
                return
            else:
                pass
        elif message.id < msg:
                await app.send_message(my, "Нечего не смог найти")
                return
        else:
            await app.send_message(my, "Ошибка")
            return

def chech_int(msg):
    if isinstance(msg, int):
        return int(msg)
    else:
        return msg