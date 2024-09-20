from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
import json
from utils.agents import get_UA
from utils.claimer_logs import logger
from requests.exceptions import HTTPError
import datetime as dt

@Client.on_message(filters.command(["pocketfi","pocket", "switch"], prefixes=pref_p)& filters.me)
async def pocketfi(client, message):
     user_id = str((await client.get_me()).id)
     session = requests.Session()
     session.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "Connection": "keep-alive",
            "Origin": "https://pocketfi.app",
            "Referer": "https://pocketfi.app/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": '"Android"',
            "User-Agent": get_UA(user_id)
        })
     web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('pocketfi_bot'),
            bot=await client.resolve_peer('pocketfi_bot'), #
            platform='android',
            from_bot_menu=True,
            url='https://pocketfi.app/mining'
        ))
     auth_url = web_view.url
     token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
     session.headers['Telegramrawdata'] = token
     try:
      resp = session.get("https://gm.pocketfi.org/mining/getUserMining")
      err = resp.raise_for_status()
      data_dict = json.loads(resp.text)
     except HTTPError as err:
      if err.response.status_code == 502:
        await message.edit_text(f"Сервер вернул ошибку 502. Скрипт остановлен.")
        return
     user = data_dict.get('userMining')
     balance = round(float(user.get('gotAmount')), 2)
     speed = user.get('speed')
     dee = user.get('dttmLastClaim')
     ts = round(dt.datetime.now().timestamp() * 1000)
     dead = user.get('dttmClaimDeadline')
     need_time = (dead - ts) / 1000
     timest = dt.datetime.fromtimestamp(dee / 1000)
     time_stop = timest.strftime("%m-%d %H:%M:%S")
     resp = session.get('https://bot.pocketfi.org/mining/taskExecuting')
     resp_json = resp.json()
     claim = resp_json['tasks']['daily'][0]['doneAmount']
     resp = session.get("https://gm.pocketfi.org/mining/guilds/3")
     data_dict = json.loads(resp.text)
     your_top = data_dict.get('userRank')
     await asyncio.sleep(2)
     text = ""
     try:
        if need_time < 3600:
            resp = session.post('https://gm.pocketfi.org/mining/claimMining')
            data_dict = json.loads(resp.text)
        try:
            mininge = float(data_dict.get('miningAmount'))
            new_balance = round(float(data_dict.get('gotAmount')), 2)
            mining = new_balance - balance
            text = f"\n<emoji id=5427009714745517609>✅</emoji> Собрал {mining} $SWITCH ({mininge})"
        except:
                pass
        if claim == 0:
            text = "\n<emoji id=5427009714745517609>✅</emoji> Ежедневный бонус собран"
            resp = session.post(url='https://bot.pocketfi.org/boost/activateDailyBoost', json={}) 
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - PocketFi\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance} $SWITCH\n⛏ Добывает - {speed} $SWITCH в час.\n<emoji id=5409008750893734809>🏆</emoji> Ты находишься на {your_top} месте{text}")
     except requests.exceptions.HTTPError as err:
        if err.response.status_code == 502:
            await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>   Error: 502 Bad Gateway -  PocketFi server is unavailable.")
            return
        else:
            await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Error: {err.response.status_code} - {err}")
            return

@Client.on_message(filters.command(["apocketfi", "apocket", "aswitch"], prefixes=pref_p)& filters.me)
async def pocketfiauto(client, message):
    with open('users.json', 'r') as f:
            data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_pocket" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_pocket']
        if auto:
            data[user_id]['auto_pocket'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор PocketFI - выключен") 
        else:
            data[user_id]['auto_pocket'] = True
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор PocketFI - включен") 
            asyncio.create_task(auto_pock(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_pocket'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор PocketFI - выключен")
    await asyncio.sleep(3)
    await msg.delete()


async def auto_pock(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
            if user_id in data and "auto_pocket" in data[user_id]:
                with open('users.json', 'r') as f:
                    data = json.load(f)
                    auto = data[user_id]['auto_pocket']
                if auto:
                    session = requests.Session() 
                    try:
                        session = requests.Session()
                        session.headers.update({
                            "Accept": "*/*",
                            "Accept-Encoding": "gzip, deflate",
                            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                            "Connection": "keep-alive",
                            "Origin": "https://pocketfi.app",
                            "Referer": "https://pocketfi.app/",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "cross-site",
                            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                            "sec-ch-ua-mobile": "?1",
                            "sec-ch-ua-platform": '"Android"',
                            "User-Agent": get_UA(user_id)
                        })
                        web_view = await client.invoke(RequestWebView(
                            peer=await client.resolve_peer('pocketfi_bot'),
                            bot=await client.resolve_peer('pocketfi_bot'), #
                            platform='android',
                            from_bot_menu=True,
                            url='https://pocketfi.app/mining'
                        ))
                        auth_url = web_view.url
                        token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                        session.headers['Telegramrawdata'] = token
                        try:
                            resp = session.get("https://gm.pocketfi.org/mining/getUserMining")
                            err = resp.raise_for_status()
                            data_dict = json.loads(resp.text)
                        except HTTPError as err:
                            if err.response.status_code == 502:
                                print("err")
                                await asyncio.sleep(12)
                                pass
                        user = data_dict.get('userMining')
                        balance = round(float(user.get('gotAmount')), 2)
                        speed = user.get('speed')
                        ts = round(dt.datetime.now().timestamp() * 1000)
                        dee = user.get('dttmLastClaim')
                        dead = user.get('dttmClaimDeadline')
                        need_time = (dead - ts) / 1000
                        timest = dt.datetime.fromtimestamp(dee / 1000)
                        time_stop = timest.strftime("%m-%d %H:%M:%S")
                        resp = session.get('https://bot.pocketfi.org/mining/taskExecuting')
                        resp_json = resp.json()
                        claim = resp_json['tasks']['daily'][0]['doneAmount']
                        resp = session.get("https://gm.pocketfi.org/mining/guilds/3")
                        data_dict = json.loads(resp.text)
                        your_top = data_dict.get('userRank')
                        await asyncio.sleep(2)
                        text = ""
                        await asyncio.sleep(need_time - 30)
                        try:
                            resp = session.post('https://gm.pocketfi.org/mining/claimMining')
                            data_dict = json.loads(resp.text)
                            try:
                                mininge = float(data_dict.get('miningAmount'))
                                new_balance = round(float(data_dict.get('gotAmount')), 2)
                                mining = new_balance - balance
                                text = f"Собрал {mining} $SWITCH ({mininge})"
                            except:
                                    pass
                            if claim == 0:
                                text = "Ежедневный бонус собран"
                                resp = session.post(url='https://bot.pocketfi.org/boost/activateDailyBoost', json={})
                            print(f'POCKETFI - Done ({user_name})')
                            await client.read_chat_history('pocketfi_bot')
                            logger(f"ID {user_id}({user_name}) PocketFi claimed. Info: Balance - {balance} Top - {your_top}| {text}")
                        except requests.exceptions.HTTPError as err:
                            print("err")
                    except Exception as e:
                        await client.send_message("me", f"**У вас нету бота @pocketfi_bot, запустить его и автомизацию (.apocketfi) {e}**")
                        with open('users.json', 'r') as f:
                            data = json.load(f)
                            data[user_id]['auto_pocket'] = True
                        with open('users.json', 'w') as f:
                            json.dump(data, f, indent=2)
                        break
                else:
                    break
            else:
                with open('users.json', 'r') as f:
                    data = json.load(f)
                    data[user_id]['auto_pocket'] = False
                with open('users.json', 'w') as f:
                    json.dump(data, f, indent=2)