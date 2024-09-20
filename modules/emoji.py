from pyrogram import Client, filters, types, enums
from config import pref_p
import asyncio
@Client.on_message(filters.command(["gep"], prefixes=pref_p) & filters.me)
async def get_prem_id(client, message):
        emjs = message.reply_to_message.entities
        emj = message.reply_to_message.text
        for item in emjs:
            emj_id = item.custom_emoji_id
        await message.edit_text(f"`{emj}` - `{emj_id}`")

@Client.on_message(filters.command("status", prefixes=pref_p) & filters.me)
async def premst(client, message):
 emoji = int(message.command[1])
 try:
     await client.set_emoji_status(types.EmojiStatus(custom_emoji_id=emoji))
     await message.edit_text(f"<emoji id=5021905410089550576>✅</emoji>Ваш статус был изменен")
     await asyncio.sleep(3)
     await message.delete()
 except Exception as e:
     await message.edit_text(f"<emoji id=5019523782004441717>❌</emoji> Произошла ошибка:{e}")
     await asyncio.sleep(3)
     await message.delete()