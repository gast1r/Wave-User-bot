from pyrogram import Client, filters, enums
from config import pref_p
import time
import asyncio, random
import re
import requests
from urllib.parse import quote
#Made for answer for callback
@Client.on_message(filters.command("inlinee", prefixes=pref_p) & filters.me)
async def inline(client, message):
 await client.send_inline_bot_result("ffmemesbot", results.query_id, "⏬️")
 await client.request_callback_answer("ffmemesbot", message.id-2, "next")



#Maybe used to complete task in bots for cheating in react(If the user wishes, the income is entirely his)|Может быть использован для ботов по накрутки реакцей (Пожеланию пользователяб доход полностью его)
@Client.on_message(filters.command("react", prefixes=pref_p) & filters.me)
async def reaction(client, message):
 emoji = message.command[3]
 id = int(message.command[2])
 channel = message.command[1]
 await client.send_reaction(channel, id, emoji)
 print("Done")
 
@Client.on_message(filters.command("channels", prefixes=pref_p) & filters.me)
async def channel(client, message):
    print(await client.get_personal_channels())

@Client.on_message(filters.command("nchats", prefixes=pref_p) & filters.me)
async def chats_my(client, message):   
    chats = await client.get_nearby_chats(55.750628, 37.616976)
    print(chats)
    
@Client.on_message(filters.command("btest", prefixes=pref_p) & filters.me)
async def bithday(client, message):   
    await client.update_birthday(day=1, month=1, year=1900)

@Client.on_message(filters.command("statusoff", prefixes=pref_p) & filters.me)
async def status(client, message): 
    await message.delete()
    while True:
        await client.update_status(offline=True)
        await asyncio.sleep(5)


@Client.on_message(filters.command("effects", prefixes=pref_p) & filters.me)
async def eff(client, message): 
    await client.get_available_effects()

@Client.on_message(filters.command("ccmsg", prefixes=pref_p) & filters.me)
async def ccopy(client, message):   
    msg = await client.copy_message('me', 'me', 123)


@Client.on_message(filters.command("efr", prefixes=pref_p) & filters.me)
async def days(client, message):   
    days = await client.get_account_ttl()
    print(days)
    
@Client.on_message(filters.command("unreaaaad", prefixes=pref_p) & filters.me)
async def unread(client, message):   
    Client.mark_chat_unread(chat_id=message.chat.id)
    
@Client.on_message(filters.command("unr", prefixes=pref_p) & filters.me)
async def archv(client, message): 
    async for dialog in client.get_dialogs(from_archive=True):
        print(dialog.chat.first_name or dialog.chat.title)
    count = await client.get_dialogs_count()
    print(count)

@Client.on_message(filters.command("msgcount", prefixes=pref_p) & filters.me)
async def msg_counter(client, message):
    match = re.search(r"\.(?:msgcount|act)\s+(.*)", message.text)
    if match == None: 
        msg_count = await client.get_chat_history_count(message.chat.id)
        print(msg_count)
        return
    tag = match.group(1)
    msg_count = await client.get_chat_history_count(tag)
    print(msg_count)


@Client.on_message(filters.command("doctorweb", prefixes=pref_p) & filters.me)
async def msg_counter(client, message):
    url = "https://free.drweb.ru/download+cureit+free/"
    mail = ''
    name = ['Арина', 'Арина', 'Сергей', 'Ева', 'Алиса', 'Амелия', 'Роман', 'Вероника ']
    surname = ['Третьякова', 'Гончарова', 'Синицын', 'Виноградова', 'Калугин', 'Харитонова', 'Крылов']
    data = f'name={quote(name[random.randint(0, len(name) - 1)])}&surname={quote(surname[random.randint(0, len(surname) - 1)].split[1])}&email={quote(mail)}&i_agree=1'
    print(data)
    resp = requests.post(url, data=data)
    print(resp.text)
    print(resp.status_code)