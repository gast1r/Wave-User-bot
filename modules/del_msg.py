from pyrogram import Client, filters
from config import pref_p
import asyncio
@Client.on_message(filters.command(["dd","дд"], prefixes=pref_p) & filters.me)
async def delete(client, message):
    await client.delete_messages(message.chat.id, message.reply_to_message_id)
    await message.delete()

@Client.on_message(filters.command(["dd-","дд-"], prefixes=pref_p) & filters.me)
async def delandedit(client, message):
    await client.delete_messages(message.chat.id, message.reply_to_message_id)
    await message.delete()


@Client.on_message(filters.command(["purge","очистить"], prefixes=pref_p) & filters.me)
async def purge(app, message):
    chunk = []
    async for msg in app.get_chat_history(
        chat_id=message.chat.id,
        limit=message.id - message.reply_to_message.id + 1,
    ):
        if msg.id < message.reply_to_message.id:
            break
        chunk.append(msg.id)
        if len(chunk) >= 100:
            await app.delete_messages(message.chat.id, chunk)
            chunk.clear()
            await asyncio.sleep(1)

    if len(chunk) > 0:
        await app.delete_messages(message.chat.id, chunk)


@Client.on_message(filters.command(["purge me","очистить я"], prefixes=pref_p) & filters.me)
async def etst(app, message):
    my_id = str((await app.get_me()).id)
    chunk = []
    async for msg in app.get_chat_history(
        chat_id=message.chat.id,
        limit=message.id - message.reply_to_message.id + 1,
    ):
        other_id = str(msg.from_user.id)
        if msg.id < message.reply_to_message.id:
            break
        if  my_id == other_id:
            chunk.append(msg.id)
        if len(chunk) >= 100:
            if  my_id == other_id:
                await app.delete_messages(message.chat.id, chunk)
                chunk.clear()
                await asyncio.sleep(1)

    if len(chunk) > 0:
        await app.delete_messages(message.chat.id, chunk)