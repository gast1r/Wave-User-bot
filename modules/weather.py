from pyrogram import Client, filters
from config import pref_p, api_w
import requests
import re


@Client.on_message(filters.command(["погода","weather"], prefixes=pref_p) & filters.me)
async def weather(app, message):
    match = re.search(r"\.(?:погода|weather)\s+(.*)", message.text)
    city = match.group(1)
    emoji_num = 0
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={api_w}&units=metric")
    data = res.json()
    if res.status_code == 200:
        ftemp = data['main']['feels_like']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        desc = data['weather'][0]['description']
        try:
            country = data['sys']['country']
        except Exception:
            country = "none"
            pass
        emoji_list = ["☁️", "<emoji id=5458375663339709450>⛅️</emoji>", "<emoji id=5469947168523558652>☀️</emoji>", "🌧️", "🌩️", "❄️"]
        if desc == "ясно":
           emoji_num = 2
        elif desc == "пасмурно":
           emoji_num = 0
        elif desc == "гроза":
           emoji_num = 4
        elif desc == "дождь":
           emoji_num = 3
        elif desc == "облачно с прояснениями":
           emoji_num = 1
        elif desc == "переменная облачность":
           emoji_num = 1
        if temp >=8:
            em = "<emoji id=5458786979472744976>🌡️</emoji>"
        elif temp<7:
            em ="<emoji id=5456573443522700218>🥶</emoji>"
        await message.edit_text(f"<emoji id=5019551308449841888>☀️</emoji> Погода в {city}\n"
        f"{em} Температура {temp}°\n"
        f"{em} Ощущаеться как {ftemp}°\n"
        f"<emoji id=5429386382143406909>💧</emoji> Влажность {humidity}%\n"
        f"<emoji id=5411285332668720752>🏳️</emoji> Страна - {country}\n"
        f"<emoji id=5427090528850164238>😣</emoji> Давление {pressure} Pa\n"
        f"<emoji id=5458747839435776472>🌬</emoji> Скорость ветра {wind} М\n"
        f"{emoji_list[emoji_num]} Описание: {desc}.")
    elif res.status_code == 404:
        await message.edit_text(f"<emoji id=5019523782004441717>❌</emoji> {city} не был найден")