from pyrogram import Client, filters
from config import pref_p
import re
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
import json
import urllib.parse
import random
import string
from utils.agents import generate_random_user_agent
import websockets

@Client.on_message(filters.command(["gs", "gsn"], prefixes=pref_p)& filters.me)
async def gsn(client, message):
    session = requests.Session()
    session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br, zstd", "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7", "Cache-Control": "no-cache", "Connection": "keep-alive", "Host": "cheatbox.site:3000", "Pragma": "no-cache", "Reffer": "https://cheatbox.site:3000/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"})
    await asyncio.sleep(1)
    web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('gsncoin_bot'),
            bot=await client.resolve_peer('gsncoin_bot'),
            platform='android',
            from_bot_menu=False,
            url='https://cheatbox.site:3000/'
        ))
    random_t= generate_random_string(7)
    print(web_view.url)
    params = {"EIO": '4', "transport": "polling", "t": random_t}
    resp = session.get("https://cheatbox.site:3000/socket.io/", params=params)
    json_part = resp.text[1:]
    parsed_data = json.loads(json_part)
    sid = parsed_data['sid']
    print(f"sid: {sid}")
    random_t = generate_random_string(7)
    params = {"EIO": '4', "transport": "polling", "t": random_t, "sid": sid}
    random_t= generate_random_string(7)
    async with websockets.connect(f"wss://cheatbox.site:3000/socket.io/?EIO=4&transport=websocket&sid={sid}") as websocket:
        await websocket.send("333")
        click = str(create_random_click())
        await websocket.send(click)
        i = 10
        while websocket.open:
            await websocket.send(click)
            await asyncio.sleep(0.5)
            i -= 1
        print("done")

def generate_random_string(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_random_click():
    event = [
        "[main] click",
        {
            "user": {
                "id": "827935645",
                "first_name": "Атри 🦴",
                "last_name": "",
                "username": "atri227",
                "language_code": "ru",
                "is_premium": True, 
                "allows_write_to_pm":True  
            },
            "object": {
                "position": {
                    "x": random.randint(0, 500),  
                    "y": str(random.randint(0, 500))  
                },
                "center": {
                    "x": "187.5",
                    "y": "150.09375"
                },
                "delta": {
                    "x": round(random.uniform(-1.0, 1.0), 3), 
                    "y": round(random.uniform(-1.0, 1.0), 3) 
                },
                "rotate": {
                    "x": round(random.uniform(-10.0, 10.0), 3),  
                    "y": round(random.uniform(-10.0, 10.0), 3)  
                }
            }
        }
    ]
    
    return event