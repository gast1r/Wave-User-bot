from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
import requests
import asyncio
from utils.agents import get_UA
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
from random import randint as rnd
from datetime import datetime as dt, timedelta, timezone
import json


@Client.on_message(filters.command(["dogiators", "диабло"], prefixes=pref_p)& filters.me)
async def dogiators(client, message):
    user_data = await client.get_me()
    user_id = str(user_data.id)
    web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('@Dogiators_bot'),
            bot=await client.resolve_peer('@Dogiators_bot'), 
            platform='android',
            from_bot_menu=True,
            url='https://tte.dogiators.com/'
        ))
    auth_url = web_view.url
    print(auth_url)
    token = auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0]
    session = requests.Session()
    session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
    session.headers.update({
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "Content-Type": "application/json",
                "Origin": "https://tte.dogiators.com",
                "Priority": "u=1, i",
                "Referer": "https://tte.dogiators.com/",
                'Host': 'tte.dogiators.com',
                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": '"Android"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": get_UA(user_id)
                })
    payload = {"taps":0,"profit":0,"ts":0,"timezone":"Europe/Moscow"}
    resp = session.post(f'https://tte.dogiators.com/api/v1/profile/init?tg_data={token}&referral_code=GNXy3YN1jN3JX4UZ', json=payload)
    profile = json.loads(resp.text)['result']['profile']
    balance = round(profile['balance'])
    cur_enr = profile['cur_energy']
    max_enr = profile['max_energy']
    level = profile['level']
    PPH = profile['profit_per_hour']
    PPT = profile['profit_per_tap']
    eps = profile['energy_recovery_per_sec']
    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Dogiators\n<emoji id=5375296873982604963>💰</emoji> Баланс: {balance} $\n<emoji id=5420315771991497307>🔥</emoji> Энергии - {cur_enr}/{max_enr}\n<emoji id=5472030678633684592>💸</emoji> Доход в час - {PPH}")
    while True:
        if cur_enr >= eps * 6:
            timestamp = round(dt.now().timestamp())
            taps = rnd(100,200)
            payload = {"taps":taps,"profit":taps * PPT,"timestamp":timestamp}
            resp = session.patch(f'https://tte.dogiators.com/api/v1/profile/update?tg_data={token}&referral_code=GNXy3YN1jN3JX4UZ', json=payload)
            profile = json.loads(resp.text)['result']['profile']
            cur_enr = profile['cur_energy']
            balance = round(profile['balance'])
            await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Dogiators\n<emoji id=5375296873982604963>💰</emoji> Баланс: {balance} $\n<emoji id=5420315771991497307>🔥</emoji> Энергии - {cur_enr}/{max_enr}\n<emoji id=5472030678633684592>💸</emoji> Доход в час - {PPH}")
            await asyncio.sleep(5)
        else:
            break
    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Dogiators\n<emoji id=5375296873982604963>💰</emoji> Баланс: {balance} $\n<emoji id=5420315771991497307>🔥</emoji> Энергии - {cur_enr}/{max_enr}\n<emoji id=5472030678633684592>💸</emoji> Доход в час - {PPH}\n<emoji id=5427009714745517609>✅</emoji> Покликал")
    resp = session.get(f'https://tte.dogiators.com/api/v1/quests/info?tg_data={token}')
    task = json.loads(resp.text)['result']
    daily_date = task['daily_rewards']['reward_days']
    for item in daily_date:
        if item['is_completed'] == False and item['is_current'] == True:
            resp = session.post(f'https://tte.dogiators.com/api/v1/quests/daily-reward/claim?tg_data={token}')
            value = item['value']
    for item in task['subscriptions_state']:
        if item['is_completed'] == False:
            payload = {"type": item['type']}
            resp = session.post(f'https://tte.dogiators.com/api/v1/quests/subscribe/claim?tg_data={token}', json=payload)


@Client.on_message(filters.command(["adogiators", "autodogiators", "адиабло"], prefixes=pref_p)& filters.me)
async def automatic_dogiators(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_dogiators" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_dogiators']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_dogiators'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор Dogiators- выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_dogiators'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор Dogiators - включен") 
            await auto_dogiators(client, user_id, user_name)
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_dogiators'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор Dogiators - выключен")
    await asyncio.sleep(2)
    await msg.delete()


async def auto_dogiators(client, user_id, user_name):
  while True:
        with open('users.json', 'r') as f:
          data = json.load(f)
        if user_id in data and "auto_dogiators" in data[user_id]:
            with open('users.json', 'r') as f:
              data = json.load(f)
              auto = data[user_id]['auto_dogiators']
            if auto:
                try:
                    web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('@Dogiators_bot'),
                        bot=await client.resolve_peer('@Dogiators_bot'), 
                        platform='android',
                        from_bot_menu=True,
                        url='https://tte.dogiators.com/'
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
                                "Content-Type": "application/json",
                                "Origin": "https://tte.dogiators.com",
                                "Priority": "u=1, i",
                                "Referer": "https://tte.dogiators.com/",
                                'Host': 'tte.dogiators.com',
                                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                                "sec-ch-ua-mobile": "?1",
                                "sec-ch-ua-platform": '"Android"',
                                "Sec-Fetch-Dest": "empty",
                                "Sec-Fetch-Mode": "cors",
                                "Sec-Fetch-Site": "same-origin",
                                "User-Agent": get_UA(user_id)
                                })
                    payload = {"taps":0,"profit":0,"ts":0,"timezone":"Europe/Moscow"}
                    resp = session.post(f'https://tte.dogiators.com/api/v1/profile/init?tg_data={token}&referral_code=GNXy3YN1jN3JX4UZ', json=payload)
                    profile = json.loads(resp.text)['result']['profile']
                    balance = round(profile['balance'])
                    cur_enr = profile['cur_energy']
                    max_enr = profile['max_energy']
                    level = profile['level']
                    PPH = profile['profit_per_hour']
                    PPT = profile['profit_per_tap']
                    eps = profile['energy_recovery_per_sec']
                    while True:
                        if cur_enr >= eps * 6:
                            timestamp = round(dt.now().timestamp())
                            taps = rnd(100,200)
                            payload = {"taps":taps,"profit":taps * PPT,"timestamp":timestamp}
                            resp = session.patch(f'https://tte.dogiators.com/api/v1/profile/update?tg_data={token}&referral_code=GNXy3YN1jN3JX4UZ', json=payload)
                            profile = json.loads(resp.text)['result']['profile']
                            cur_enr = profile['cur_energy']
                            balance = round(profile['balance'])
                            await asyncio.sleep(5)
                        else:
                            break
                    logger(f"{user_name} | Dogiators | Баланс: {balance} $ | Энергии - {cur_enr}/{max_enr} | Доход в час - {PPH} | Покликал")
                    resp = session.get(f'https://tte.dogiators.com/api/v1/quests/info?tg_data={token}')
                    task = json.loads(resp.text)['result']
                    daily_date = task['daily_rewards']['reward_days']
                    for item in daily_date:
                        if item['is_completed'] == False and item['is_current'] == True:
                            resp = session.post(f'https://tte.dogiators.com/api/v1/quests/daily-reward/claim?tg_data={token}')
                            value = item['value']
                    for item in task['subscriptions_state']:
                        if item['is_completed'] == False:
                            payload = {"type": item['type']}
                            resp = session.post(f'https://tte.dogiators.com/api/v1/quests/subscribe/claim?tg_data={token}', json=payload)
                    await asyncio.sleep(rnd(3600, 10800))
                except Exception as ex:
                    print(ex, 'Dogiators')
            else:
                    break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_dogiators'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)