from pyrogram import Client, filters
from config import pref_p


@Client.on_message(filters.command(["dice","d", "кубик"], prefixes=pref_p) & filters.me)
async def emoji(app, message):
    await message.delete()
    await app.send_dice(message.chat.id)


@Client.on_message(filters.command(["basket","баскетбол", "bs"], prefixes=pref_p) & filters.me)
async def basket(app, message):
    await message.delete()
    await app.send_dice(message.chat.id, "🏀")


@Client.on_message(filters.command(["bowling","боулинг", "bl"], prefixes=pref_p) & filters.me)
async def bowling(app, message):
    await message.delete()
    f = await app.send_dice(message.chat.id, "🎳")
    #f.dice.value

@Client.on_message(filters.command(["slots","слоты"], prefixes=pref_p) & filters.me)
async def slots(app, message):
    await message.delete()
    f = await app.send_dice(message.chat.id, "🎰")
    #f.dice.value


@Client.on_message(filters.command(["football","футбол", "футболл", "футбик"], prefixes=pref_p) & filters.me)
async def football(app, message):
    await message.delete()
    f = await app.send_dice(message.chat.id, "⚽️")