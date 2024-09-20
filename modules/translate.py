import re
from pyrogram import Client, filters
from config import pref_p
import asyncio
from deep_translator import GoogleTranslator
from langdetect import detect
@Client.on_message(filters.command(["tr", "перевод"], prefixes=pref_p)& filters.me)
async def translate_text(client, message):
    if message.reply_to_message is None:
        match = re.search(r"\.(?:tr|перевод)\s+(.*)", message.text)
        if match:  
            word = match.group(1).strip()  
            language = detect(word)
            if language == "en":
                translator = GoogleTranslator(source='en', target='ru')
            elif language == "ru" or language == "bg":
                translator = GoogleTranslator(source='auto', target='en')
            else:
                translator = GoogleTranslator(source='auto', target='ru')
            if word == "":
                await message.edit_text("<emoji id=5019523782004441717>❌</emoji> Не предоставлен текст для перевода.")
                await asyncio.sleep(2)
                await message.delete()
            else:
                try:
                    translation = translator.translate(word) 
                    await message.edit_text(f"{translation}")  
                except Exception as e:
                    print(f"Ошибка при переводе слова '{word}': {e}")
                    await message.edit_text("<emoji id=5019523782004441717>❌</emoji> Произошла ошибка при выполнении перевода.")
                    await asyncio.sleep(5)
                    await message.delete()
        else:
            message.edit_text("<emoji id=5019523782004441717>❌</emoji> Не удалось найти текст для перевода.")
            await asyncio.sleep(2)
            await message.delete()

    else:
        if  message.reply_to_message.caption != None:
            word = message.reply_to_message.caption
        elif message.reply_to_message.text != None:
            word = message.reply_to_message.text
        else:
            msg = await message.edit_text("<emoji id=5019523782004441717>❌</emoji> Произошла ошибка. Не найден текст!")
            await asyncio.sleep(4)
            await msg.delete()
            return
        try:
            language = detect(word)
            if language == "en":
                translator = GoogleTranslator(source='en', target='ru')
            elif language == "ru" or language == "bg":
                translator = GoogleTranslator(source='auto', target='en')
            else:
                translator = GoogleTranslator(source='auto', target='ru')
            translation = translator.translate(word)
            await message.edit_text(f"{translation}")
        except Exception as e:
            print(e)
            msg = await message.edit_text("<emoji id=5019523782004441717>❌</emoji> Произошла ошибка при выполнении перевода.")
            await asyncio.sleep(2)
            await msg.delete()