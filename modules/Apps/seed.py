from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
import json
import random
from utils.proxy import GET_PROXY
from utils.claimer_logs import logger
from utils.agents import get_UA
from datetime import datetime, timedelta, timezone


@Client.on_message(filters.command(["seed", "сид"], prefixes=pref_p)& filters.me)
async def seed(client, message):
    try:
        user_id = str((await client.get_me()).id)
        session = requests.Session()
        session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "cache-control": "no-cache", "Origin": "https://cf.seeddao.org", "pragma": "no-cache", "Priority": "u=1,i", "Referer": "https://cf.seeddao.org/", "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "User-Agent": get_UA(user_id)})
        web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('seed_coin_bot'),
            bot=await client.resolve_peer('seed_coin_bot'),
            platform='android',
            from_bot_menu=True,
            url='https://cf.seeddao.org'
        ))
        auth_url = web_view.url
        token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
        session.headers['telegram-data'] = token
        resp = session.get('https://elb.seeddao.org/api/v1/login-bonuses')
        info = json.loads(resp.text)
        dateb_claim = info['data'][0]['timestamp']
        if dateb_claim == None:
            session.post('https://elb.seeddao.org/api/v1/login-bonuses') #daily
            session.get('https://elb.seeddao.org/api/v1/streak-reward')
            info = json.loads(resp.text)
            if 'id' in info:
                id_streak = info['id']
                session.post('https://elb.seeddao.org/api/v1/streak-reward', json={"streak_reward_ids":[id_streak]})
                text += "\n<emoji id=5427009714745517609>✅</emoji> Собрал ежд. бонус"
        resp = session.get('https://elb.seeddao.org/api/v1/profile/balance')
        info = json.loads(resp.text)
        balance = round(float(info['data'] / 100000000),2)
        resp = session.get('https://elb.seeddao.org/api/v1/profile2')
        info = json.loads(resp.text)
        pickup_at = datetime.fromisoformat(dateb_claim)
        pick_up = pickup_at + timedelta(days=1)
        now_utc = datetime.now(timezone.utc)
        text = ''
        if now_utc > pick_up:
            session.post('https://elb.seeddao.org/api/v1/login-bonuses') #daily
            session.get('https://elb.seeddao.org/api/v1/streak-reward')
            info = json.loads(resp.text)
            if 'id' in info:
                id_streak = info['id']
                session.post('https://elb.seeddao.org/api/v1/streak-reward', json={"streak_reward_ids":[id_streak]})
                text += "\n<emoji id=5427009714745517609>✅</emoji> Собрал ежд. бонус"
        last_claim = info['data']['last_claim']
        pickup_at = datetime.fromisoformat(last_claim)
        pick_up = pickup_at + timedelta(hours=4)
        now_utc = datetime.now(timezone.utc)
        if now_utc > pick_up:
            resp = session.post('https://elb.seeddao.org/api/v1/seed/claim')
            text += '\n<emoji id=5427009714745517609>✅</emoji> Собрал майнинг'
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Seed\n<emoji id=5375296873982604963>💰</emoji> Баланс: {balance} $SEED{text}")
    except Exception as e:
        print(e)
        return

@Client.on_message(filters.command(["aseed", "асид"], prefixes=pref_p)& filters.me)
async def automa_seed(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_seed" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_seed']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_seed'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор 1Win - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_seed'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор 1Win - включен") 
            await auto_seed(client, user_id, user_name)
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_seed'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор 1Win - выключен")
    await asyncio.sleep(2)
    await msg.delete()


async def auto_seed(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
        if user_id in data and "auto_seed" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_seed']
            if auto:
                try:
                    user_id = str((await client.get_me()).id)
                    session = requests.Session()
                    session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "cache-control": "no-cache", "Origin": "https://cf.seeddao.org", "pragma": "no-cache", "Priority": "u=1,i", "Referer": "https://cf.seeddao.org/", "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "User-Agent": get_UA(user_id)})
                    web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('seed_coin_bot'),
                        bot=await client.resolve_peer('seed_coin_bot'),
                        platform='android',
                        from_bot_menu=True,
                        url='https://cf.seeddao.org'
                    ))
                    auth_url = web_view.url
                    token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                    session.proxies = {
                        "http": f"https://{GET_PROXY(user_id)}"
                    }
                    text = ''
                    session.headers['telegram-data'] = token
                    resp = session.get('https://elb.seeddao.org/api/v1/login-bonuses')
                    info = json.loads(resp.text)
                    dateb_claim = info['data'][0]['timestamp']
                    if dateb_claim == None:
                        session.post('https://elb.seeddao.org/api/v1/login-bonuses') #daily
                        session.get('https://elb.seeddao.org/api/v1/streak-reward')
                        info = json.loads(resp.text)
                        if 'id' in info:
                            id_streak = info['id']
                            session.post('https://elb.seeddao.org/api/v1/streak-reward', json={"streak_reward_ids":[id_streak]})
                    resp = session.get('https://elb.seeddao.org/api/v1/profile/balance')
                    info = json.loads(resp.text)
                    balance = round(float(info['data'] / 100000000),2)
                    resp = session.get('https://elb.seeddao.org/api/v1/profile2')
                    info = json.loads(resp.text)
                    last_claim = info['data']['last_claim']
                    pickup_at = datetime.fromisoformat(dateb_claim)
                    pickup_at = pickup_at + timedelta(days=1)
                    now_utc = datetime.now(timezone.utc)
                    if now_utc > pickup_at:
                        session.post('https://elb.seeddao.org/api/v1/login-bonuses') #daily
                        session.get('https://elb.seeddao.org/api/v1/streak-reward')
                        info = json.loads(resp.text)
                        if 'id' in info:
                            id_streak = info['id']
                            session.post('https://elb.seeddao.org/api/v1/streak-reward', json={"streak_reward_ids":[id_streak]})
                            text += "| Собрал ежд. бонус "
                    pickup_at = datetime.fromisoformat(last_claim)
                    pickup_at = pickup_at + timedelta(hours=4)
                    now_utc = datetime.now(timezone.utc)
                    if now_utc > pickup_at:
                        resp = session.post('https://elb.seeddao.org/api/v1/seed/claim')
                        text += '| Собрал майнинг '
                        wait_time = 3 * 60 * 60 + 30
                    else:
                        wait_time = pickup_at - now_utc
                    print("Done - SEED")
                    logger(f"{user_name} Seed | Balance: {balance} $SEED {text}")
                    await asyncio.sleep(wait_time.total_seconds())
                except Exception as e:
                    print("SEED -",e)
                    return
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_seed'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)