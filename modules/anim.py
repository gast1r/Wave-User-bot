from pyrogram import Client, filters
from config import pref_p
import asyncio
import random
@Client.on_message(filters.command(["часы", "clock"], prefixes=pref_p) & filters.me)
async def clock(client, message):
    await message.edit_text("🕛")
    await asyncio.sleep(1)
    await message.edit_text("🕐")
    await asyncio.sleep(1)
    await message.edit_text("🕑")
    await asyncio.sleep(1)
    await message.edit_text("🕒")
    await asyncio.sleep(1)
    await message.edit_text("🕓")
    await asyncio.sleep(1)
    await message.edit_text("🕔")
    await asyncio.sleep(1)
    await message.edit_text("🕕")
    await asyncio.sleep(1)
    await message.edit_text("🕖")
    await asyncio.sleep(1)
    await message.edit_text("🕗")
    await asyncio.sleep(1)
    await message.edit_text("🕘")
    await asyncio.sleep(1)
    await message.edit_text("🕙")
    await asyncio.sleep(1)
    await message.edit_text("🕚")
    await asyncio.sleep(1)
    await message.edit_text("🕛")
    await asyncio.sleep(1)
    await message.edit_text("Bye⏳")
    await asyncio.sleep(2)
    await message.edit_text("Bye⌛️")
    await asyncio.sleep(1)
    await message.edit_text("Bye👋")
    await asyncio.sleep(3)
    await message.delete()

@Client.on_message(filters.command(["hack", "взлом"], prefixes=pref_p) & filters.me )
async def hack(client, message):
    await message.edit_text("💻 Взлом аккаунта...")
    await asyncio.sleep(2)
    await message.edit_text("⚠️ Брутфорсим пароль")
    await asyncio.sleep(2)
    rnd = random.randint(1, 2)
    if rnd == 1:
        await message.edit_text("<emoji id=5021905410089550576>✅</emoji> Пароль подошел")
        await asyncio.sleep(1)
        await message.edit_text("⏳ Меняю пароль.")
        await asyncio.sleep(2)
        await message.edit_text("⏳ Меняю пароль..")
        await asyncio.sleep(2)
        await message.edit_text("⏳ Меняю пароль...")
        await asyncio.sleep(2)
        await message.edit_text("<emoji id=5021905410089550576>✅</emoji> Пароль сменен")
        await asyncio.sleep(2)
        await message.edit_text("🤐 Качаем данные с переписок.")
        await asyncio.sleep(2)
        await message.edit_text("🤐 Качаем данные с переписок..")
        await asyncio.sleep(2)
        await message.edit_text("🤐 Качаем данные с переписок...")
        await asyncio.sleep(1)
        await message.edit_text("<emoji id=5021905410089550576>✅</emoji> Данные скачены")
        await asyncio.sleep(1)
        await message.edit_text("🪄 Запаковаем данные.")
        await asyncio.sleep(1)
        await message.edit_text("🪄 Запаковаем данные..")
        await asyncio.sleep(1)
        await message.edit_text("🪄 Запаковаем данные...")
        await asyncio.sleep(2)
        await message.edit_text("<emoji id=5021905410089550576>✅</emoji> Данные запакованны")
        await asyncio.sleep(1)
        await message.edit_text("💣 Загружаем на сервер")
        await asyncio.sleep(2)
        await message.edit_text("<emoji id=5021905410089550576>✅</emoji> Данные загружены на сервер")
        await asyncio.sleep(2)
        await message.edit_text("<emoji id=5203996991054432397>🎁</emoji> Отправляем подарок")
        await asyncio.sleep(2)
        await message.edit_text("k")
        await message.delete()
        
    else:
        await message.edit_text("<emoji id=5019523782004441717>❌</emoji> Неудачно")
        await asyncio.sleep(2)
        await message.delete()