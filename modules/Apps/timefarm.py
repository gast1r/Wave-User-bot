from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
import json
from utils.agents import get_UA
from utils.claimer_logs import logger
from datetime import datetime, timedelta


@Client.on_message(filters.command(["timefarm", "тайм"], prefixes=pref_p)& filters.me)
async def timefarm(client, message):
    try:
        user_id = str((await client.get_me()).id)
        session = requests.Session()
        session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "Content-type": "application/json", "Origin": "https://timefarm.app", "Priority": "u=1,i", "Referer": "https://timefarm.app/", "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "User-Agent": get_UA(user_id)})
        web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('TimeFarmCryptoBot'),
            bot=await client.resolve_peer('TimeFarmCryptoBot'),
            platform='android',
            from_bot_menu=True,
            url='https://timefarm.app'
        ))
        auth_url = web_view.url
        token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        payload = {"initData": str(token), "platform": "android"}
        resp = session.post("https://tg-bot-tap.laborx.io/api/v1/auth/validate-init/v2", json=payload)
        info = json.loads(resp.text)
        auth = info["token"]
        balance = info["balanceInfo"]["balance"]
        autofarm = info["balanceInfo"]["autofarm"]
        coinsfarm = info["farmingInfo"]["farmingReward"]
        farmsec = info["farmingInfo"]["farmingDurationInSec"]
        level = info["info"]["level"]
        session.headers["Authorization"] = f"Bearer {auth}"
        session.headers.pop("Content-type", None)
        resp = session.get("https://tg-bot-tap.laborx.io/api/v1/farming/info")
        info = json.loads(resp.text)
        try:
            active = info["activeFarmingStartedAt"]
        except:
            resp = session.post("https://tg-bot-tap.laborx.io/api/v1/farming/start", json={})
            await asyncio.sleep(3)
            resp = session.get("https://tg-bot-tap.laborx.io/api/v1/farming/info")
            info = json.loads(resp.text)
            active = info["activeFarmingStartedAt"]
        farmingReward = info["farmingReward"]
        multiplier = info["multiplier"]
        date_object = datetime.strptime(active, "%Y-%m-%dT%H:%M:%S.%fZ")
        timestamp = int(date_object.timestamp())
        claim_timestamp = timestamp + 14480 + 10800
        current_timestamp = int(datetime.now().timestamp())
        difference = claim_timestamp - current_timestamp
        session.headers["Content-type"] = "application/json"
        text = ""
        if difference <= 0:
            resp = session.post("https://tg-bot-tap.laborx.io/api/v1/farming/finish", json={})
            resp = session.post("https://tg-bot-tap.laborx.io/api/v1/farming/start", json={})
            reward = farmingReward * multiplier
            text += f"\n<emoji id=5427009714745517609>✅</emoji> Собрали {reward} $SECOND"
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Time Farm\n<emoji id=5375296873982604963>💰</emoji> Баланс: {balance}$SECOND\n<emoji id=5364105043907716258>🆙</emoji>Уровень: {level} {text}")
        get_tasks(session)
    except Exception as e:
        await message.edit_text(f"Кажется вы еще не зарегистрировались в TimeFarm @TimeFarmCryptoBot")
        print(e)

def get_tasks(session):
    resp = session.get('https://tg-bot-tap.laborx.io/api/v1/tasks')
    info = json.loads(resp.text)
    for task in info:
        task_id = task["id"]
        task_title = task["title"]
        task_type = task["type"]
        if task_type == "TELEGRAM":
                continue
        if "submission" in task.keys():
            status = task["submission"]["status"]
            if status == "CLAIMED":
                continue

            if status == "COMPLETED":
                    resp = session.post(f"https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims")
                    if resp.text.lower() == "ok":
                        continue

        resp = session.post(f"https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions")
        if resp.text != "ok":
                continue

        resp = session.post(f"https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}")
        status = json.loads(resp.text)["submission"]["status"]
        if status != "COMPLETED":
                continue

        resp = session.post(f"https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims")
        if resp.text == "ok":
                continue


async def auto_timefarm(client, user_id, user_name):
  while True:
        with open('users.json', 'r') as f:
          data = json.load(f)
        if user_id in data and "auto_timefarm" in data[user_id]:
            with open('users.json', 'r') as f:
              data = json.load(f)
              auto = data[user_id]['auto_timefarm']
            if auto:
                try:
                    session = requests.Session()
                    session.headers.update({"Accept": "*/*", "Accept-Encoding": "gzip, deflate", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "Content-type": "application/json", "Origin": "https://timefarm.app", "Priority": "u=1,i", "Referer": "https://timefarm.app/", "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?1", "sec-ch-ua-platform": '"Android"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "User-Agent": get_UA(user_id)})
                    web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('TimeFarmCryptoBot'),
                        bot=await client.resolve_peer('TimeFarmCryptoBot'),
                        platform='android',
                        from_bot_menu=True,
                        url='https://timefarm.app'
                    ))
                    auth_url = web_view.url
                    token = unquote(auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                    payload = {"initData": str(token), "platform": "android"}
                    resp = session.post("https://tg-bot-tap.laborx.io/api/v1/auth/validate-init/v2", json=payload)
                    info = json.loads(resp.text)
                    auth = info["token"]
                    balance = info["balanceInfo"]["balance"]
                    autofarm = info["balanceInfo"]["autofarm"]
                    coinsfarm = info["farmingInfo"]["farmingReward"]
                    farmsec = info["farmingInfo"]["farmingDurationInSec"]
                    level = info["info"]["level"]
                    session.headers["Authorization"] = f"Bearer {auth}"
                    session.headers.pop("Content-type", None)
                    resp = session.get("https://tg-bot-tap.laborx.io/api/v1/farming/info")
                    info = json.loads(resp.text)
                    try:
                        active = info["activeFarmingStartedAt"]
                    except:
                        resp = session.post("https://tg-bot-tap.laborx.io/api/v1/farming/start", json={})
                        await asyncio.sleep(3)
                        resp = session.get("https://tg-bot-tap.laborx.io/api/v1/farming/info")
                        info = json.loads(resp.text)
                        active = info["activeFarmingStartedAt"]
                    farmingReward = info["farmingReward"]
                    multiplier = info["multiplier"]
                    date_object = datetime.strptime(active, "%Y-%m-%dT%H:%M:%S.%fZ")
                    timestamp = int(date_object.timestamp())
                    claim_timestamp = timestamp + farmsec + 10800
                    current_timestamp = int(datetime.now().timestamp())
                    difference = claim_timestamp - current_timestamp 
                    session.headers["Content-type"] = "application/json"
                    text = ""
                    get_tasks(session)
                    if difference <= 0:
                        resp = session.post("https://tg-bot-tap.laborx.io/api/v1/farming/finish", json={})
                        resp = session.post("https://tg-bot-tap.laborx.io/api/v1/farming/start", json={})
                        reward = farmingReward * multiplier
                        text += f"| Собрали {reward} $SECOND"
                        resp = session.get("https://tg-bot-tap.laborx.io/api/v1/farming/info")
                        info = json.loads(resp.text)
                        active = info["activeFarmingStartedAt"]
                        date_object = datetime.strptime(active, "%Y-%m-%dT%H:%M:%S.%fZ")
                        timestamp = int(date_object.timestamp())
                        claim_timestamp = timestamp + farmsec
                        current_timestamp = int(datetime.now().timestamp())
                        difference = current_timestamp - claim_timestamp
                        logger(f"{user_name} Time Farm | Баланс: {balance} $SECOND | Уровень: {level} {text}")
                    await asyncio.sleep(difference)
                except Exception as e:
                    print(e)
                    break
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_timefarm'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)


@Client.on_message(filters.command(["atimefarm", "автотаймфарм", "атаймфарм"], prefixes=pref_p)& filters.me)
async def timefarm_autom(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_timefarm" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_timefarm']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_timefarm'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"❌ Автоматический сбор Time Farm - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_timefarm'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"✅ Автоматический сбор Time Farm - включен") 
            asyncio.create_task(auto_timefarm(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_timefarm'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"❌ Автоматический сбор Time Farm - выключен")
    await asyncio.sleep(2)
    await msg.delete()