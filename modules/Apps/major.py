from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from random import randint
from urllib.parse import unquote
import asyncio
import json
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
from datetime import datetime as dt
import time
import requests
from utils.agents import get_UA

@Client.on_message(filters.command(["majorrt", "мажор"], prefixes=pref_p)& filters.private)
async def major(client, message):
    user_data = await client.get_me()
    user_id = str(user_data.id)
    session = requests.Session()
    session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
    session.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Priority": "u=1, i",
            "Referer": "https://major.bot/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
            "Sec-Ch-Ua-mobile": "?1",
            "Sec-Ch-Ua-platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": get_UA(user_id)
    })
    web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('@major'),
            bot=await client.resolve_peer('@major'),
            platform='android',
            from_bot_menu=True,
            url='https://major.bot/'
        ))
    auth_url = web_view.url
    token = unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
    payload = {"init_data": token}
    resp = session.post("https://major.bot/api/auth/tg/", json=payload)
    info = json.loads(resp.text)
    token_app = info['access_token']
    session.headers['Authorization'] = f"Bearer {token_app}"
    resp = session.post('https://major.bot/api/user-visits/visit/')
    resp = session.get('https://major.bot/api/user-visits/streak/')
    info = json.loads(resp.text)
    streak = info['streak']
    resp = session.get(f"https://major.bot/api/users/{user_id}/")
    info = json.loads(resp.text)
    stars = info['rating']
    resp = session.get(f"https://major.bot/api/users/top/position/{user_id}/?")
    info = json.loads(resp.text)
    position = info['position']
    time_wait = asyncio.create_task(game_comp(session))
    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - MAJOR\n<emoji id=5375296873982604963>💰</emoji> Баланс: {stars} <emoji id=5816707898696274976>⭐️</emoji>\n<emoji id=5409008750893734809>🏆</emoji>Место в топе - {position}\n<emoji id=5424972470023104089>🔥</emoji>Стрик - {streak}")
    await mark_tasks_as_done(True, session)
    await mark_tasks_as_done(False, session)


async def mark_tasks_as_done(is_daily, session):
    url = f'https://major.bot/api/tasks/?is_daily={is_daily}'
    resp = session.get(url)
    n_daily = json.loads(resp.text)
    for item in n_daily:
        id = item['id']
        comp = item['is_completed']
        title = item['title']
        if item['type'] == 'code' and comp == False:
            resp = requests.get('https://raw.githubusercontent.com/GravelFire/TWFqb3JCb3RQdXp6bGVEdXJvdg/master/answer.py')
            try:
                code = json.loads(resp.text)['youtube'][title]
                payload = {"task_id":f"{id}","payload":{"code":code}}
                resp = session.post('https://major.bot/api/tasks/', json=payload)
            except:
                pass
        if comp == False:
            payload = {"task_id": f"{id}"}
            resp = session.post('https://major.bot/api/tasks/', json=payload)
        await asyncio.sleep(2)
    return


@Client.on_message(filters.command(["amajor", "automajor", "амажор"], prefixes=pref_p)& filters.me)
async def major_auto(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_major" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_major']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_major'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"❌ Автоматический сбор Major - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_major'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"✅ Автоматический сбор Major - включен") 
            asyncio.create_task(auto_major(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_major'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"❌ Автоматический сбор Major - выключен")
    await asyncio.sleep(2)
    await msg.delete()

async def auto_major(client, user_id, user_name):
  while True:
        with open('users.json', 'r') as f:
          data = json.load(f)
        if user_id in data and "auto_major" in data[user_id]:
            with open('users.json', 'r') as f:
              data = json.load(f)
              auto = data[user_id]['auto_major']
            if auto:
                session = requests.Session()
                session.headers.update({
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br, zstd",
                        "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                        "Priority": "u=1, i", 
                        "Referer": "https://major.bot/",
                        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                        "Sec-Ch-Ua-mobile": "?1",
                        "Sec-Ch-Ua-platform": '"Android"',
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "User-Agent": get_UA(user_id)
                })
                web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('@major'),
                        bot=await client.resolve_peer('@major'), 
                        platform='android',
                        from_bot_menu=True,
                        url='https://major.bot/'
                    ))
                auth_url = web_view.url
                token = unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                payload = {"init_data": token}
                resp = session.post("https://major.bot/api/auth/tg/", json=payload)
                text = ""
                info = json.loads(resp.text)
                token_app = info['access_token']
                session.headers['Authorization'] = f"Bearer {token_app}"
                resp = session.post('https://major.bot/api/user-visits/visit/')
                resp = session.get('https://major.bot/api/user-visits/streak/')
                info = json.loads(resp.text)
                streak = info['streak']
                resp = session.get(f"https://major.bot/api/users/{user_id}/")
                info = json.loads(resp.text)
                stars = info['rating']
                resp = session.get(f"https://major.bot/api/users/top/position/{user_id}/?")
                info = json.loads(resp.text)
                position = info['position']
                time_wait, text = await game_comp(session)
                await asyncio.sleep(5)
                await mark_tasks_as_done(True, session)
                await mark_tasks_as_done(False, session)
                current_datetime = dt.now().timestamp()
                try:
                    time_difference = time_wait - current_datetime
                except Exception as e:
                    print(e)
                logger(f"ID {user_id}({user_name}) MAJOR | Balance: {stars} $Star | Top - {position} | Streak - {streak}")
                if time_difference > 0:
                    await asyncio.sleep(time_difference + randint(10, 160))
                else:
                    await asyncio.sleep(randint(170, 500))
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_major'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
                break

async def game_comp(session):
        text = ''
        win = 0
        resp = session.get("https://major.bot/api/bonuses/coins/") #COIN
        if resp.status_code == 200:
            await asyncio.sleep(62)
            rnd_coins = randint(900, 915)
            payload = {'coins': int(rnd_coins)}
            resp = session.post('https://major.bot/api/bonuses/coins/', json=payload)
            win = rnd_coins
        else:
            info = json.loads(resp.text)
            time_wait = info['detail']['blocked_until']
        resp = session.get("https://major.bot/api/swipe_coin/") #SWIPE
        if resp.status_code != 400:
            await asyncio.sleep(62)
            rnd_coins = randint(1150, 1250)
            payload = {'coins': int(rnd_coins)}
            session.post('https://major.bot/api/swipe_coin/', json=payload)
            resp = session.get("https://major.bot/api/swipe_coin/") #SWIPE
            info = json.loads(resp.text)
            time_wait = info['detail']['blocked_until']
            win += rnd_coins
        else:
            info = json.loads(resp.text)
            time_wait = info['detail']['blocked_until']
        resp = session.get('https://major.bot/api/durov/')
        if resp.status_code != 400:
                resp = requests.get('https://raw.githubusercontent.com/GravelFire/TWFqb3JCb3RQdXp6bGVEdXJvdg/master/answer.py')
                info = json.loads(resp.text)
                if info['expires'] > int(time.time()):
                    payload = info['answer']
                    resp = session.post("https://major.bot/api/durov/", json=payload)
                    info = json.loads(resp.text)
                    win += 5000
                    resp = session.get("https://major.bot/api/durov/")
                    info = json.loads(resp.text)
                    time_wait = info['detail']['blocked_until']
        else:
            info = json.loads(resp.text)
            time_wait = info['detail']['blocked_until']
        resp = session.get("https://major.bot/api/roulette/")
        if resp.status_code != 400:
            await asyncio.sleep(15)
            resp = session.post("https://major.bot/api/roulette/")
            info = json.loads(resp.text)
            win += info['rating_award']
            resp = session.get("https://major.bot/api/roulette/")
            info = json.loads(resp.text)
            time_wait = info['detail']['blocked_until']
        else:
            info = json.loads(resp.text)
            time_wait = info['detail']['blocked_until']
        if win != 0:
            text = f"Сыграл в мини-игры +{win}"
        return time_wait, text


def check_date(timestamp):
    timestamp_datetime = dt.fromtimestamp(timestamp)
    current_date = dt.now()
    return timestamp_datetime.day == current_date.day