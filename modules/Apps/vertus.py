from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
import json
from utils.proxy import GET_PROXY
from utils.agents import get_UA
from utils.claimer_logs import logger
from datetime import datetime, timedelta, timezone


@Client.on_message(filters.command(["vertus", "вертус"], prefixes=pref_p)& filters.me)
async def vertus(client, message):
    try:
        user_id = str((await client.get_me()).id)
        session = requests.Session()
        session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
        session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "cache-control": "no-cache", "Origin": "https://thevertus.app", "Priority": "u=1,i", "Referer": "https://thevertus.app/", "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cors-site", "User-Agent": get_UA(user_id)})
        web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('Vertus_App_bot'),
            bot=await client.resolve_peer('Vertus_App_bot'),
            platform='android',
            from_bot_menu=True,
            url='https://thevertus.app/'
        ))
        auth_url = web_view.url
        token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        session.headers['Authorization'] = 'Bearer ' + token
        text = ''
        resp = session.post('https://api.thevertus.app/users/get-data', json={})
        info = json.loads(resp.text)
        balance = round(info['user']['balance'] / 100000000000000000, 6)
        active = info['user']['activated']
        storage = round(info['user']['vertStorage'] / 1000000000000000000, 2)
        daily = info['user']['dailyRewards']
        lastclaim_daily = daily['lastRewardClaimed']
        if lastclaim_daily == None:
            resp = session.post('https://api.thevertus.app/game-service/collect', json={})
        lastclaim_daily = str(lastclaim_daily)
        streak = daily['consecutiveDays']
        lastclaim_daily = daily['lastRewardClaimed']
        pickup_at = datetime.fromisoformat(lastclaim_daily)
        pickup_at = pickup_at + timedelta(days=1)
        now_utc = datetime.now(timezone.utc)
        if pickup_at > now_utc:
            resp = session.post("https://api.thevertus.app/users/claim-daily", json={})
            text += '\n<emoji id=5427009714745517609>✅</emoji> Собрал ежд. бонус'
        try:
            session.post('https://api.thevertus.app/codes/validate', json={"code":"1432"})
            print(resp.text)
        except:
            pass
        if storage >= 0.003:
            resp = session.post('https://api.thevertus.app/game-service/collect', json={})
            if resp.status_code == 201:
                text += f"\n<emoji id=5427009714745517609>✅</emoji> Собрал майнинг +{storage} VERT"
        resp = session.post('https://api.thevertus.app/users/get-data', json={})
        info = json.loads(resp.text)
        balance = round(info['user']['balance'] / 100000000000000000, 6)
        storage = round(info['user']['vertStorage'] / 1000000000000000000, 2)
        streak = info['user']['dailyRewards']['consecutiveDays']
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Vertus\n<emoji id=5375296873982604963>💰</emoji> Баланс: {balance} $SEED\n<emoji id=5420315771991497307>🔥</emoji> Стрик - {streak}\n<emoji id=5451732530048802485>⏳</emoji>Хранилище - {storage} {text}")
    except Exception as e:
        print(e)
        return


@Client.on_message(filters.command(["avertus", "авертус"], prefixes=pref_p)& filters.me)
async def vertus_automa(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_vertus" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_vertus']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_vertus'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор Vertus - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_vertus'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор Vertus - включен") 
            await auto_vertus(client, user_id, user_name)
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_vertus'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор Vertus - выключен")
    await asyncio.sleep(2)
    await msg.delete()


async def auto_vertus(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
        if user_id in data and "auto_vertus" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_vertus']
            if auto:
                try:
                    session = requests.Session()
                    session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "cache-control": "no-cache", "Origin": "https://thevertus.app", "Priority": "u=1,i", "Referer": "https://thevertus.app/", "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cors-site", "User-Agent": get_UA(user_id)})
                    web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('Vertus_App_bot'),
                        bot=await client.resolve_peer('Vertus_App_bot'),
                        platform='android',
                        from_bot_menu=True,
                        url='https://thevertus.app/'
                    ))
                    auth_url = web_view.url
                    token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                    session.headers['Authorization'] = 'Bearer ' + token
                    text = ''
                    resp = session.post('https://api.thevertus.app/users/get-data', json={})
                    info = json.loads(resp.text)
                    balance = round(info['user']['balance'] / 100000000000000000, 6)
                    active = info['user']['activated']
                    storage = round(info['user']['vertStorage'] / 1000000000000000000, 2)
                    daily = info['user']['dailyRewards']
                    if  daily['lastRewardClaimed'] == None:
                        resp = session.post("https://api.thevertus.app/users/claim-daily", json={})
                        resp = session.post('https://api.thevertus.app/users/get-data', json={})
                        info = json.loads(resp.text)
                        daily = info['user']['dailyRewards']
                    lastclaim_daily = daily['lastRewardClaimed']
                    pickup_at = datetime.fromisoformat(lastclaim_daily)
                    pickup_at = pickup_at + timedelta(days=1)
                    now_utc = datetime.now(timezone.utc)
                    if pickup_at < now_utc:
                        resp = session.post("https://api.thevertus.app/users/claim-daily", json={})
                    streak = daily['consecutiveDays']
                    pickup_at = datetime.fromisoformat(lastclaim_daily)
                    pickup_at = pickup_at + timedelta(days=1)
                    now_utc = datetime.now(timezone.utc)
                    if pickup_at > now_utc:
                        resp = session.post("https://api.thevertus.app/users/claim-daily", json={})
                        text += ' | Собрал ежд. бонус'
                    try:
                        session.post('[https://api.thevertus.app/codes/validate', json={"code":"1432"})
                        print(resp.text)
                    except:
                        pass
                    if storage >= 0.003:
                        resp = session.post('https://api.thevertus.app/game-service/collect', json={})
                        if resp == 201:
                            text += f" |  +{storage} VERT"
                            resp = session.post('https://api.thevertus.app/users/get-data', json={})
                            info = json.loads(resp.text)
                            balance = round(info['user']['balance'] / 100000000000000000, 6)
                            storage = round(info['user']['vertStorage'] / 1000000000000000000, 2)
                            streak = info['user']['dailyRewards']['consecutiveDays']
                            time = 14400
                        else:
                            time = 14400 - 5400
                    else:
                        time = 14400 - 5400
                    print("Done - Vertus")
                    logger(f"{user_name}  Vertus | Баланс: {balance} $VERT | Стрик - {streak} | Хранилище - {storage} {text}")
                    await asyncio.sleep(time)
                except Exception as e:
                    print("Vertus -",e)
                    return
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_vertus'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)