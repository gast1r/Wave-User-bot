from pyrogram import Client, filters
from config import pref_p
import os
import asyncio
import time

@Client.on_message(filters.command("chats", prefixes=pref_p) & filters.me)
async def getchats(client, message):
 lim = message.text.split(" ", 1)[1]  # Получаем тег из сообщения
 if int(lim) <= 500:
     #text = print(f"ID канала/чата {tag}")
     archived_chats =  client.get_dialogs(limit=int(lim))
     with open("chats_list.txt", "w", encoding="utf-8") as file:
        async for dialog in archived_chats:
            if dialog.chat.title == None:
                if dialog.chat.last_name == None:
                    file.write(f"Name: {dialog.chat.first_name}\n")
                else:
                    file.write(f"Name: {dialog.chat.first_name} {dialog.chat.last_name}\n")
            else:
                file.write(f"Name: {dialog.chat.title}\n")
            file.write(f"Type: {dialog.chat.type}\n")
            file.write(f"Username: {dialog.chat.username}\n")
            file.write(f"ID: {dialog.chat.id}\n")
            file.write(f"Last msg date: {dialog.top_message.date}\n")
            file.write(f"Last msg: {dialog.top_message.text}\n")
            file.write(f"Total messages: {dialog.top_message.id}\n")
            file.write(f"Protect: {dialog.top_message.has_protected_content}\n")
            file.write(f"Unread msgs: {dialog.unread_messages_count}\n")
            file.write(f"Mark: {dialog.unread_mark}\n")
            file.write(f"Pinned: {dialog.is_pinned}\n")
            file.write("\n\n")
            #print(dialog.top_message)
     await message.edit_text("Список чатов с информацей. Всего у вас чатов ~")
     await client.send_document(message.chat.id, "chats_list.txt")
     os.remove("chats_list.txt")


@Client.on_message(filters.command(["ichats", "ichat"], prefixes=pref_p) & filters.me)
async def read(client, message):
 i = 0
 all_msg = 0
 max_unread_msgs = 0
 count = await client.get_dialogs_count()
 # Получаем тег из сообщения
 archived_chats =  client.get_dialogs(limit=count)
 await message.edit_text(f"💬 Всего чатов - **{count}**.\n👀 Начинаю просматривать")
 start = time.time()
 async for dialog in archived_chats:
    if dialog.chat.title == None:
        chat = dialog.chat.first_name, dialog.chat.last_name
    else:
        chat = dialog.chat.title
    if dialog.unread_messages_count >= 1: 
        #print(f"Чат {chat} - непрочитан ({dialog.unread_messages_count})")
        i += 1
        all_msg += dialog.unread_messages_count
        if dialog.unread_messages_count > max_unread_msgs:
                max_unread_msgs = dialog.unread_messages_count
                chat_with_most_msgs = chat
                chatmost = dialog.chat.username
    finish = time.time()
    res = finish - start
    if i > 0:
        avg_time_per_chat = round(res / i, 2)
    else:
        avg_time_per_chat = 0

 finish = time.time()
 res = finish - start
 res = round(res, 2)
 await message.edit_text(f"❌ Непрочитанных чатов - **{i}/{count}**\n💬 Всего непрочитанных сообщений - **{all_msg}**\n⏳ Заняло времени на проверку - **{res}** секунд\n🕰️ Cреднее время проверки одного чата - **{avg_time_per_chat}** сек\n📊 Самый большое количество непрочитанных сообщений - **{max_unread_msgs}** в чате **[{chat_with_most_msgs}](t.me/{chatmost})**")
