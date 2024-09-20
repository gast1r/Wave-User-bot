import requests
import json
from utils.proxy import GET_PROXY
from pyrogram import Client, filters
from requests.adapters import HTTPAdapter
from config import pref_p
def get_proxy_country(proxy_address):
    headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
    }
    try:
        response = requests.get("https://www.google.com", proxies={"http": proxy_address}, timeout=5)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        return "Dead", None, None
    try:
        url = "https://2domains.ru/api/web-tools/myip"
        response = requests.get(url, headers=headers, proxies={"http": proxy_address}, timeout=5)
        print(response.text)
        info = json.loads(response.text)
        ip = info['ip']
        country = info['geo']['country']
        city = info['geo']['city']
        return country, city, ip
    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения информации о стране: {e}")
        return None, None, None

@Client.on_message(filters.command(["proxyy", "прокси"], prefixes=pref_p)& filters.me)
async def get_proxy(client, message):
    user_data = await client.get_me()
    user_id = str(user_data.id)
    proxy = GET_PROXY(user_id)
    proxy_address = f"http://38.29.32.240:3128"
    print(proxy)
    country, city, ip  = get_proxy_country(proxy_address)
    if country == "Dead":
        await message.edit_text(f"Ошибка проверки прокси.\n\n<emoji id=5472146462362048818>💡</emoji> Может быть прокси умер.")
    if country:
        await message.edit_text(f"🏳️ Страна прокси {ip}: {country}\n🏙 Город прокси {ip}: {city}")
    else:
        await message.edit_text(f"Не удалось определить страну прокси.")