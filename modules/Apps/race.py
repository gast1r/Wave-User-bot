from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote, quote, parse_qs
import requests
import asyncio
from utils.agents import get_UA
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
import random, json

@Client.on_message(filters.command(["racer", "гонка"], prefixes=pref_p)& filters.me)
async def race(client, message):
    user_data = await client.get_me()
    user_id = str(user_data.id)
    web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('@Racememe_bot'),
            bot=await client.resolve_peer('@Racememe_bot'), 
            platform='android',
            from_bot_menu=True,
            url='https://racing-tg.web.app/'
        ))
    auth_url = web_view.url
    token = auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0]
    session = requests.Session()
    session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
    session.headers.update({
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "Origin": "https://racing-tg.web.app",
                "Priority": "u=1, i",
                "Referer": "https://racing-tg.web.app/",
                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": '"Android"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": get_UA(user_id)
                })
    text = ''
    resp = session.post(f'https://racing-tg-p12o.onrender.com/race/claimDailyRewardAmount?tgInitData={token}')
    if resp.status_code == 200:
        text += '\n<emoji id=5427009714745517609>✅</emoji> Собрал ежд. бонус!'
    resp = session.get(f'https://racing-tg-p12o.onrender.com/user?tgInitData={token}')
    data = json.loads(resp.text)
    balance = round(data['user']['distance']['lastDistanceAmount'])
    fuel = round(data['user']['fuel']['lastFuelAmount'])
    restore = data['user']['fuel']['numberOfRestores']
    fuel_per_sec = data['user']['fuel']['litersPerSecond']
    max_fuel = data['user']['fuel']['maxCapacity']
    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **$RACE TO BILLION**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} $RACE**\n<emoji id=5431449001532594346>⚡️</emoji> Бензин - {fuel}/{max_fuel}\n<emoji id=5453918011272470772>🏎</emoji> Гоню...{text}")
    while True:
        if fuel < 3 and restore != 6:
            session.get(f'https://racing-tg-p12o.onrender.com/booster/restoreFullTank?tgInitData={token}')
            fuel = data['user']['fuel']['lastFuelAmount']
        if fuel < 3 and restore == 6:
            text += '\n<emoji id=5465665476971471368>❌</emoji> Потратил все бустеры!'
            await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **$RACE TO BILLION**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} $RACE**\n<emoji id=5431449001532594346>⚡️</emoji> Бензин - {fuel}/{max_fuel}\n<emoji id=5453918011272470772>🏎</emoji> Гоню...{text}")
            break
        rand = random.randint(100, 200)
        payload = {"numberOfMeters":rand,"numberOfLiters":rand * 0.005}
        resp = session.post(f'https://racing-tg-p12o.onrender.com/race/addDistance?tgInitData={token}', json=payload)
        resp = session.get(f'https://racing-tg-p12o.onrender.com/user?tgInitData={token}')
        data = json.loads(resp.text)
        fuel = round(data['user']['fuel']['lastFuelAmount'])
        balance = round(data['user']['distance']['lastDistanceAmount'])
        await asyncio.sleep(1)
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **$RACE TO BILLION**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} $RACE**\n<emoji id=5431449001532594346>⚡️</emoji> Бензин - {fuel}/{max_fuel}\n<emoji id=5453918011272470772>🏎</emoji> Гоню...{text}")
        
        
        
async def auto_race(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
        if user_id in data and "auto_racer" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_racer']
            if auto:
                try:
                    web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('@Racememe_bot'),
                        bot=await client.resolve_peer('@Racememe_bot'), 
                        platform='android',
                        from_bot_menu=True,
                        url='https://racing-tg.web.app/'
                    ))
                    auth_url = web_view.url
                    token = auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0]
                    session = requests.Session()
                    session.proxies = {
                            "http": f"https://{GET_PROXY(user_id)}"
                        }
                    session.headers.update({
                                "Accept": "*/*",
                                "Accept-Encoding": "gzip, deflate, br, zstd",
                                "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                                "Origin": "https://racing-tg.web.app",
                                "Priority": "u=1, i",
                                "Referer": "https://racing-tg.web.app/",
                                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                                "sec-ch-ua-mobile": "?1",
                                "sec-ch-ua-platform": '"Android"',
                                "Sec-Fetch-Dest": "empty",
                                "Sec-Fetch-Mode": "cors",
                                "Sec-Fetch-Site": "cross-site",
                                "User-Agent": get_UA(user_id)
                                })
                    text = ''
                    resp = session.post(f'https://racing-tg-p12o.onrender.com/race/claimDailyRewardAmount?tgInitData={token}')
                    if resp.status_code == 200:
                        text += ' | Собрал еждю бонус!'
                    resp = session.get(f'https://racing-tg-p12o.onrender.com/user?tgInitData={token}')
                    data = json.loads(resp.text)
                    balance = round(data['user']['distance']['lastDistanceAmount'])
                    fuel = round(data['user']['fuel']['lastFuelAmount'])
                    restore = data['user']['fuel']['numberOfRestores']
                    fuel_per_sec = data['user']['fuel']['litersPerSecond']
                    max_fuel = data['user']['fuel']['maxCapacity']
                    while True:
                        if fuel < 3 and restore != 6:
                            session.get(f'https://racing-tg-p12o.onrender.com/booster/restoreFullTank?tgInitData={token}')
                            fuel = data['user']['fuel']['lastFuelAmount']
                        if fuel < 3 and restore == 6:
                            text += ' | Потратил все бустеры!'
                            logger(f"{user_name} | Race - (cooldown). Info: Balance - {balance} Energy - {fuel} {text}")
                            await asyncio.sleep(180 / fuel_per_sec)
                            text = ''
                            break
                        rand = random.randint(100, 200)
                        payload = {"numberOfMeters":rand,"numberOfLiters":rand * 0.005}
                        resp = session.post(f'https://racing-tg-p12o.onrender.com/race/addDistance?tgInitData={token}', json=payload)
                        resp = session.get(f'https://racing-tg-p12o.onrender.com/user?tgInitData={token}')
                        data = json.loads(resp.text)
                        fuel = round(data['user']['fuel']['lastFuelAmount'])
                        balance = round(data['user']['distance']['lastDistanceAmount'])
                        await asyncio.sleep(1)
                except:
                    break
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_racer'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)


@Client.on_message(filters.command(["arace", "агонка"], prefixes=pref_p)& filters.me)
async def racer_auto(client, message):
    with open('users.json', 'r') as f:
            data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_racer" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_racer']
        if auto:
            data[user_id]['auto_racer'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Автоматимизация $RACE - выключен") 
        else:
            data[user_id]['auto_racer'] = True
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text("<emoji id=5427009714745517609>✅</emoji> Автоматимизация $RACE - включен") 
            asyncio.create_task(auto_race(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_racer'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Автоматимизация $RACE - выключен")
    await asyncio.sleep(3)
    await msg.delete()