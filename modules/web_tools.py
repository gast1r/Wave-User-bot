from pyrogram import Client, filters
from config import pref_p
import re
import requests
from bs4 import BeautifulSoup
import qrcode
import os
import asyncio


@Client.on_message(filters.command(["html","хтмл"], prefixes=pref_p) & filters.me)
async def html(client, message):
    try:
        match = re.search(r"\.(?:html|хтмл)\s+(.*)", message.text)
        url = match.group(1)
    except:
        await message.edit_text("❌ Ошибка")
        await asyncio.sleep(3)
        await message.delete()
        return
    response = requests.get(url)
    site = url.split("/")[2]
    await message.edit_text("❓ Получаем данные...")
    soup = BeautifulSoup(response.content, "html.parser")
    name_file = site + "_source.html"
    with open(name_file, "w", encoding="utf-8") as file:
        file.write(str(soup))
    await message.delete()
    await client.send_document(message.chat.id, name_file)
    os.remove(name_file)


@Client.on_message(filters.command(["qr","qr"], prefixes=pref_p) & filters.me)
async def qr(client, message):
    try:
        match = re.search(r"\.(?:qr|qr)\s+(.*)", message.text)
        url = match.group(1)
    except:
        await message.edit_text("❌ Ошибка")
        await asyncio.sleep(3)
        await message.delete()
        return
    await message.delete()
    response = requests.get(url)
    img = qrcode.make(url)
    type(img)  # qrcode.image.pil.PilImage
    img.save("qr.png")
    await client.send_photo(message.chat.id, "qr.png")
    os.remove("qr.png")

@Client.on_message(filters.command(["findhtml","найдихтмл"], prefixes=pref_p) & filters.me)
async def findhtml(client, message):
    try:
        split_t = message.text.split()
        print(split_t)
        url = split_t[1]
        tag = split_t[2]
        classs = split_t[3]
    except:
        await message.edit_text("❌ Ошибка")
        await asyncio.sleep(3)
        await message.delete()
        return
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
#print(soup)
    try:
        test = soup.find(tag, class_=classs)
        await message.edit_text(f"Tag - {tag} Id/Class - {classs}\n{test}")
    except:
        pass
    test = soup.find(tag, id_=classs)