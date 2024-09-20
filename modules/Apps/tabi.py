from pyrogram import Client, filters, utils
def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"
utils.get_peer_type = get_peer_type_new
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
from datetime import datetime as dt
import json
from utils.agents import get_UA
from utils.claimer_logs import logger
import random

@Client.on_message(filters.command(["tabi", "таби"], prefixes=pref_p)& filters.me)
async def tabi(client, message):
    try:
        user_id = str((await client.get_me()).id)
        session = requests.Session()
        session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br, zstd", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "Cache-Control": "no-cache", "Content-Length": "0", "Content-type": "application/json","Host": "api.tabibot.com","Origin": "https://miniapp.tabibot.com","Pragma": "no-cache", "Referer": "https://miniapp.tabibot.com","sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "User-Agent": get_UA(user_id)})
        web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('tabizoobot'),
            bot=await client.resolve_peer('tabizoobot'),
            platform='android',
            from_bot_menu=True,
            url='https://api.tabibot.com'
        ))
        auth_url = web_view.url
        token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        session.headers['Rawdata'] = token
        resp = session.get("https://api.tabibot.com/api/user/v1/profile", allow_redirects=False)
        data = json.loads(resp.text)
        user = data['data']['user']
        balance = user.get("coins")
        streak = user.get("streak")
        level = user.get("level")
        datedaily = user.get("checkInDate")
        resp = session.get("https://api.tabibot.com/api/mining/v1/info")
        if resp.text == None:
            await message.edit_text("Вы не зарегистрированы в @tabizoobot")
            await asyncio.sleep(3)
            await message.delete()
        data = json.loads(resp.text)
        data = data['data']['mining_data']
    except Exception as e:
            print(e)
            await message.edit_text("**У вас нету бота @tabizoobot, запустить его**")
            return
    earn = data.get("rate")
    earnen = data.get("current")
    limit = data.get("top_limit")
    next_claim = data.get("next_claim_timestamp") / 1000
    today = round(dt.today().timestamp()  * 1000)
    print(today)
    print(next_claim)
    claim = next_claim - today 
    if claim <= 0:
        resp = session.post("https://api.tabibot.com/api/mining/v1/claim")
    today = dt.today()
    now_date = today.strftime("%Y-%m-%d")
    if datedaily == now_date:
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - TabiZoo\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance}\n💵 Заработано - {earnen}/{limit}\n<emoji id=5420315771991497307>🔥</emoji> Стрик - {streak}\n<emoji id=5364105043907716258>🆙</emoji> Уровень - {level} клейма\n<emoji id=5472030678633684592>💸</emoji> Зарабатываешь - {earn} в час")
    else:
        resp = session.post("https://api.tabibot.com/api/user/v1/check-in")
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - TabiZoo\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance}\n💵 Заработано - {earnen}/{limit}\n<emoji id=5420315771991497307>🔥</emoji> Стрик - {streak}\n<emoji id=5364105043907716258>🆙</emoji> Уровень - {level}\n<emoji id=5472030678633684592>💸</emoji> Зарабатываешь - {earn} в час\n✅ Забрал ежд. бонус")



@Client.on_message(filters.command(["atabi", "autotabi"], prefixes=pref_p)& filters.me)
async def tabi_auto(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_tabi" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_tabi']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_tabi'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор Tabizoo - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_tabi'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор Tabizoo - включен") 
            await auto_tabi(client, user_id, user_name)
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_tabi'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор tabizoo - выключен")
    await asyncio.sleep(3)
    await msg.delete()


       
async def auto_tabi(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
        if user_id in data and "auto_tabi" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_tabi']
            if auto:
                try:
                    session = requests.Session()
                    session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br, zstd", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "Cache-Control": "no-cache", "Content-Length": "0", "Content-type": "application/json","Host": "api.tabibot.com","Origin": "https://miniapp.tabibot.com","Pragma": "no-cache", "Referer": "https://miniapp.tabibot.com","sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "User-Agent": get_UA(user_id)})
                    web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('tabizoobot'),
                        bot=await client.resolve_peer('tabizoobot'),
                        platform='android',
                        from_bot_menu=True,
                        url='https://api.tabibot.com'
                    ))
                    auth_url = web_view.url
                except Exception as e:
                    print(e)
                    await client.send_message("me", "**У вас нету бота @tabizoobot, запустить его и автомизацию (.atabi)**")
                    with open('users.json', 'r') as f:
                        data = json.load(f)
                        data[user_id]['auto_tabi'] = False
                    with open('users.json', 'w') as f:
                        json.dump(data, f, indent=2)
                        break
                token = unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                session.headers['Rawdata'] = token
                resp = session.get("https://api.tabibot.com/api/mining/v1/info")
                data = json.loads(resp.text)
                data = data['data']['mining_data']
                next_claim = data.get("next_claim_timestamp") / 1000
                today = round(dt.today().timestamp()  * 1000)
                claim = next_claim - today
                resp = session.get("https://api.tabibot.com/api/user/v1/profile", allow_redirects=False)
                data = json.loads(resp.text)
                user = data['data']['user']
                datedaily = user.get("checkInDate")
                balance = user.get("coins")
                streak = user.get("streak")
                if claim <= 0:
                    resp = session.post("https://app.tabibot.com/api/mining/v1/claim")
                today = dt.today()
                now_date = today.strftime("%Y-%m-%d")
                if datedaily != now_date:
                    resp = session.post("https://app.tabibot.com/api/user/v1/check-in")
                    daily = "Claiming daily"
                    pass
                trnd = random.randint(10, 60)
                if claim <= 0 or datedaily != now_date:

                    logger(f"ID {user_id}({user_name}) TabiZoo claimed. Info: Balance - {balance} Streak - {streak} Daily - {daily}")
                await asyncio.sleep(next_claim + trnd)
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_tabi'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)