from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
from utils.agents import get_UA
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
import random, hashlib, json, math
import datetime as dt
import time
import cloudscraper
scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session\]
@Client.on_message(filters.command(["1winn", "1вин"], prefixes=pref_p)& filters.me)
async def win_token(client, message):
    user_data = await client.get_me()
    user_id = str(user_data.id)
    session = requests.Session()
    session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Cache-Control": "no-cache",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary5f5zke0EWZObLj8i",
            "Origin": "https://cryptocklicker-frontend-rnd-prod.100hp.app",
            "Priority": "u=1, i",
            "Pragma": "no-cache",
            "Referer": "https://cryptocklicker-frontend-rnd-prod.100hp.app/",
            'Host': 'crypto-clicker-backend-go-prod.100hp.app',
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": get_UA(user_id),
            'x-user-id': user_id
        })
    web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('@token1win_bot'),
            bot=await client.resolve_peer('@token1win_bot'), 
            platform='android',
            from_bot_menu=True,
            url='https://cryptocklicker-frontend-rnd-prod.100hp.app/'
        ))
    auth_url = web_view.url
    token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
    token = token.replace("&auth_date", "&chat_instance=4159477297939709361&chat_type=sender&auth_date")  
    resp = session.post("https://crypto-clicker-backend-go-prod.100hp.app/game/start", params=token)
    print(resp)
    print(resp.text)
    auth = json.loads(resp.text)
    token = auth['token']
    energy = auth['currentEnergy']
    energy_limit = auth['energyLimit']
    profit = auth['totalPassiveProfit']
    session.headers['Authorization'] = f"Bearer {token}"
    session.headers['Accept'] = "*/*"
    session.headers.pop("Content-type", None)
    resp = session.get('https://crypto-clicker-backend-go-prod.100hp.app/user/balance')
    bal = json.loads(resp.text)
    PH = bal['miningPerHour']
    CPC = bal['coinsPerClick']
    balance = bal['coinsBalance']
    resp = session.get('https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward')
    daily = json.loads(resp.text)
    id = daily['days']
    daily_collect = daily['days'][0]['isCollected']
    if daily_collect == False:
        session.post('https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward')
    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **1Win Token**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} 1WIN**\n<emoji id=5472030678633684592>💸</emoji> Заработок в час - {PH} 1WIN\n<emoji id=5431449001532594346>⚡️</emoji> Энергии - {energy}/{energy_limit}")
    earned = 0
    while True:
        if energy != 0:
            rand = random.randint(30,100)
            earned += rand
            payload = {"tapsCount": rand}
            resp = session.post('https://crypto-clicker-backend-go-prod.100hp.app/tap', json=payload)
            resp = session.get('https://crypto-clicker-backend-go-prod.100hp.app/user/balance')
            bal = json.loads(resp.text)
            energy = bal['currentEnergy']
            balance = bal['coinsBalance']
            await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **1Win Token**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} 1WIN**\n<emoji id=5472030678633684592>💸</emoji> Заработок в час - {PH} 1WIN\n<emoji id=5431449001532594346>⚡️</emoji> Энергии - {energy}/{energy_limit}\n<emoji id=5469718869536940860>👆</emoji> Тапаю кота...")
            await asyncio.sleep(2)
        else:
            resp = session.get('https://crypto-clicker-backend-go-prod.100hp.app/energy/bonus')
            bonus = json.loads(resp.text)
            stnu = bonus['seconds_to_next_use']
            remaining = bonus['remaining']
            if stnu == 0 and remaining != 0:
                session.post('https://crypto-clicker-backend-go-prod.100hp.app/energy/bonus')
                energy = energy_limit
            else:
                break
    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **1Win Token**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} 1WIN**\n<emoji id=5472030678633684592>💸</emoji> Заработок в час - {PH} 1WIN\n<emoji id=5431449001532594346>⚡️</emoji> Энергии - {energy}/{energy_limit}\n<emoji id=5431449001532594346>⚡️</emoji> Энергия закончилась +{earned} 1WIN")

@Client.on_message(filters.command(["a1win", "а1вин"], prefixes=pref_p)& filters.me)
async def win_automatic(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_win" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_win']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_win'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор 1Win - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_win'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор 1Win - включен") 
            await auto_win_token(client, user_id, user_name)
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_win'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор 1Win - выключен")
    await asyncio.sleep(2)
    await msg.delete()

async def auto_win_token(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
        if user_id in data and "auto_win" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_win']
            if auto:
                session = requests.Session()
                session.headers.update({
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Encoding": "gzip, deflate, br, zstd",
                        "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryTDrse2BR7BA0e7dOl",
                        "content-length": "44",
                        "Origin": "https://cryptocklicker-frontend-rnd-prod.100hp.app",
                        "Priority": "u=1, i",
                        "Referer": "https://cryptocklicker-frontend-rnd-prod.100hp.app/",
                        'Host': 'crypto-clicker-backend-go-prod.100hp.app',
                        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                        "sec-ch-ua-mobile": "?1",
                        "sec-ch-ua-platform": '"Android"',
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-site",
                        "User-Agent": get_UA(user_id),
                        'x-user-id': user_id
                    })
                web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('@token1win_bot'),
                        bot=await client.resolve_peer('@token1win_bot'), 
                        platform='android',
                        from_bot_menu=True,
                        url='https://cryptocklicker-frontend-rnd-prod.100hp.app/'
                    ))
                auth_url = web_view.url
                print(auth_url)
                token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                resp = session.post(f'https://crypto-clicker-backend-go-prod.100hp.app/game/start?{token}')
                print(resp.text)
                print(resp)
                return
                auth = json.loads(resp.text)
                token = auth['token']
                energy = auth['currentEnergy']
                energy_limit = auth['energyLimit']
                profit = auth['totalPassiveProfit']
                session.headers['Authorization'] = f"Bearer {token}"
                session.headers['Accept'] = "*/*"
                session.headers.pop("Content-type", None)
                resp = session.get('https://crypto-clicker-backend-go-prod.100hp.app/user/balance')
                bal = json.loads(resp.text)
                PH = bal['miningPerHour']
                CPC = bal['coinsPerClick']
                resp = session.get('https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward')
                daily = json.loads(resp.text)
                daily_collect = daily['days'][0]['isCollected']
                if daily_collect == False:
                    session.post('https://crypto-clicker-backend-go-prod.100hp.app/tasks/everydayreward')
                earned = 0
                while True:
                    if energy != 0:
                        rand = random.randint(30,100)
                        earned += rand
                        payload = {"tapsCount": rand}
                        resp = session.post('https://crypto-clicker-backend-go-prod.100hp.app/tap', json=payload)
                        resp = session.get('https://crypto-clicker-backend-go-prod.100hp.app/user/balance')
                        bal = json.loads(resp.text)
                        energy = bal['currentEnergy']
                        balance = bal['coinsBalance']
                        await asyncio.sleep(2)
                    else:
                        resp = session.get('https://crypto-clicker-backend-go-prod.100hp.app/energy/bonus')
                        bonus = json.loads(resp.text)
                        stnu = bonus['seconds_to_next_use']
                        remaining = bonus['remaining']
                        if stnu == 0 and remaining != 0:
                            session.post('https://crypto-clicker-backend-go-prod.100hp.app/energy/bonus')
                            energy = energy_limit
                        else:
                            break
                print(f'1WIN - Done ({user_name})')
                logger(f"{user_name} 1Win Token | Balance - {balance} 1WIN | PHR - {PH} 1WIN | Energy - {energy}/{energy_limit} | Energy +{earned} 1WIN (+{profit})")
                await asyncio.sleep(3600 + random.randint(10, 120))
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_win'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)