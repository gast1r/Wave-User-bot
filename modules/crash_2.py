from pyrogram import Client, filters
from config import pref_p

@Client.on_message(filters.command(["c2","crash2", "краш2"], prefixes=pref_p) & filters.me)
async def sdblum(client, message):
 start = 0
 max = 1001
 f = ""
 await message.delete()
 while start < int(max):
       #print(start)
       start += 1
       f += f"{start}\n"
 msg = await client.send_message(message.chat.id, f)
 await msg.delete()
