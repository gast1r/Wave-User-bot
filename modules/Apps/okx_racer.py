from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
import json
from utils.agents import get_UA
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
from requests.exceptions import HTTPError
import random
import datetime as dt
import time
import re


@Client.on_message(filters.command(["okx", "окс"], prefixes=pref_p)& filters.me)
async def okx_info(client, message):
    user_data = await client.get_me()
    user_id = str(user_data.id)
    session = requests.Session()
    session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
    session.headers.update({
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "App-type": "web",
            "Priority": "u=1, i",
            "Referer": "https://www.okx.com/mini-app/racer",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "x-cdn": "https://www.okx.com",
            "x-id-group": "1020718992969240002-c-2",
            "x-locale": "en_US",
            "x-utc": "3",
            "x-zkdex-env": "0",
            "x-site-info": "=0HOxojI5RXa05WZiwiIMFkQPx0Rfh1SPJiOiUGZvNmIsISVSJiOi42bpdWZyJye",
            "Sec-Fetch-Site": "cross-site",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "User-Agent": get_UA(user_id)
        })
    web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('OKX_official_bot'),
            bot=await client.resolve_peer('OKX_official_bot'), 
            platform='android',
            from_bot_menu=True,
            url='https://www.okx.com/mini-app/racer'
        ))
    auth_url = web_view.url
    token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
    session.headers['x-telegram-init-data'] = token
    timestamp = round(time.time() * 1000)
    params = {"t": timestamp}
    user_name = str(user_data.first_name)
    match = re.search(r"\.(?:okx|окс)\s+(.*)", message.text)
    if match == None:
        data = {"extUserName": f"{user_name}", "linkCode":""}
        resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/info", params=params, json=data)
        info = json.loads(resp.text)
        user = info["data"]
        balance = user["balancePoints"]
        Chances = user["numChances"]
        secondToRefresh = user["secondToRefresh"]
        Totalchances = user["numChancesTotal"]
        if str(secondToRefresh) == "-1":
            secondToRefresh = "Энергия полностью восстановлена!"
        else:
            secondToRefresh = 90 * (Totalchances - 1 - Chances) + secondToRefresh
        params = {"t":f"{timestamp}"}
        session.headers['Referer'] = "https://www.okx.com/mini-app/racer/tasks"
        resp = session.get("https://www.okx.com/priapi/v1/affiliate/game/racer/boosts", params=params)
        bost = json.loads(resp.text)
        data = bost["data"]
        for item in data:
            if item['id'] == 1:
                continue
        resp = session.get("https://www.okx.com/priapi/v1/affiliate/game/racer/tasks", params=params)
        task = json.loads(resp.text)
        data = task["data"]
        for item in data:
            if item['id'] == 4:
                if item["state"] == 0:
                    resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/task", params=params, json={'id': 4})
                    text_daily = "\n✅ Собрал ежд. бонус"
                else:
                     text_daily = ""
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **OKX Racer**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} Points**\n⛽️ Бензин - {Chances}/{Totalchances}\n<emoji id=5420315771991497307>🔥</emoji> До восстановления бензина - **{secondToRefresh}** {text_daily}")
        return
    text = match.group(1)
    if any(keyword in text for keyword in ["rnd", "r", "р", "рнд"]):
        await okx_race(session, message, user_name, random.randint(0, 1))
        return
    elif any(keyword in text for keyword in ["moon all", "up a", "moon a", "ап все", "вверх алл"]):
        await okx_allrace(session, message, user_name, 1)
        return
    elif any(keyword in text for keyword in ["down all", "down a", "doom all", "doom a", "все", "алл"]):
        await okx_allrace(session, message, user_name, 0)
        return
    elif any(keyword in text for keyword in ["moon", "up", "ап", "вверх"]):
        await okx_race(session, message, user_name, 1)
        return
    elif any(keyword in text for keyword in ["doom", "down", "вниз", "даун"]):
        await okx_race(session, message, user_name, 0)
        return
    elif any(keyword in text for keyword in ["all", "a", "все", "алл"]):
        await okx_allrace(session, message, user_name, random.randint(0, 1))
        return
    
    
async def okx_allrace(session, message, name, num):
    try:
        timestamp = round(time.time() * 1000)
        params = {"t": timestamp}
        resp = session.get("https://www.okx.com/priapi/v1/affiliate/game/racer/tasks", params=params)
        task = json.loads(resp.text)
        data = task["data"]
        for item in data:
            if item['id'] == 4:
                if item["state"] == 0:
                    resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/task", params=params, json={'id': 4})
                    text_daily = "\n✅ Собрал ежд. бонус"
                else:
                    text_daily = ""
        total_play = 0
        total_win = 0
        total_points = 0
        while True:
            data = {"extUserName": str(name), "linkCode": ""}
            params = {"t": round(time.time() * 1000)}
            try:
                resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/info", params=params, json=data)
                resp.raise_for_status()  
            except requests.exceptions.ConnectionError:
                await message.edit_text("Ошибка соединения.")
                await asyncio.sleep(5)  # Ждем перед повторной попыткой
            except requests.exceptions.HTTPError:
                await message.edit_text("HTTP ошибка.")
                await asyncio.sleep(5)
            info = resp.json()
            if resp.status_code != 200:
                await asyncio.sleep(2)
                continue
            user = info["data"]
            chances = user["numChances"]
            if chances == 0: 
                balance = user["balancePoints"]
                secondToRefresh = user["secondToRefresh"]
                Totalchances = user["numChancesTotal"]
                await message.edit_text("<emoji id=5467583879948803288>🎮</emoji> Игра - **OKX Racer**\n Нет бензина!\nПытаюсь использовать бустер")
                if boost(session): 
                    await message.edit_text("💥 Бустер успешно использован! Пытаемся продолжить игру...")
                    await asyncio.sleep(2)
                else:
                    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **OKX Racer**\n💎 Потратил весь бензин!\n<emoji id=5420315771991497307>🔥</emoji> Вины - {total_win}/{total_play}\n<emoji id=5472030678633684592>💸</emoji> Выиграл - {total_points}\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance} Points\n❌ Не удалось использовать бустер, у вас закончились доступные бустеры.") 
                    break
            params = {"t": round(time.time() * 1000)}
            data = {"predict": str(num)}  
            while True:
                try:
                    resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/assess", params=params, json=data)
                    resp.raise_for_status() 
                    break  
                except requests.exceptions.ConnectionError as e:
                    await message.edit_text(f"Ошибка соединения.")
                    await asyncio.sleep(4) 
                except requests.exceptions.HTTPError as e:
                    await message.edit_text(f"HTTP ошибка")
                    break
            info = resp.json()  
            user = info["data"]
            error_code = info["error_code"]
            if error_code != "0":
                await asyncio.sleep(3)
                return  
            win = user["won"]
            if win:
                total_win += 1
                total_play += 1
                beet = user["basePoint"]
                multiplier = user["multiplier"]
                total_points += beet * multiplier
                chances = user["numChance"]
            else:
                total_play += 1
            with open('global.json', 'r') as f:
                data = json.load(f)
                if "okx_games" not in data:
                    data['okx_games'] = 0
            data['okx_games'] += 1
            with open('global.json', 'w') as f:
                json.dump(data, f)
            wait_time = round(random.uniform(7.8, 8.8), 2)
            time_z = round(chances * wait_time)
            text = f"<emoji id=5467583879948803288>🎮</emoji> Игра - **OKX Racer**\n 💵 Трачу бензин...\n<emoji id=5451646226975955576>⌛️</emoji> Времени займет - {time_z} сек\n⛽️ Осталось попыток - {chances}\n<emoji id=5420315771991497307>🔥</emoji> Выиграно игр - {total_win}/{total_play}\n<emoji id=5472030678633684592>💸</emoji> Выиграл {total_points} Points"
            await message.edit_text(text)
            await asyncio.sleep(wait_time)
    except Exception as ex:
        print(ex)


async def auto_okx(client, user_id, name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
        if user_id in data and "auto_okx" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_okx']
            if auto:
                params = {"t": round(time.time() * 1000)}
                session = requests.Session()
                session.proxies = {
                    "http": f"https://{GET_PROXY(user_id)}"
                }
                session.headers.update({
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                    "App-type": "web",
                    "Priority": "u=1, i",
                    "Referer": "https://www.okx.com/mini-app/racer",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "x-cdn": "https://www.okx.com",
                    "x-id-group": "1020718992969240002-c-2",
                    "x-locale": "en_US",
                    "x-utc": "3",
                    "x-zkdex-env": "0",
                    "x-site-info": "=0HOxojI5RXa05WZiwiIMFkQPx0Rfh1SPJiOiUGZvNmIsISVSJiOi42bpdWZyJye",
                    "Sec-Fetch-Site": "cross-site",
                    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                    "sec-ch-ua-mobile": "?1",
                    "sec-ch-ua-platform": '"Android"',
                    "User-Agent": get_UA(user_id)
                })
                web_view = await client.invoke(RequestWebView(
                    peer=await client.resolve_peer('OKX_official_bot'),
                    bot=await client.resolve_peer('OKX_official_bot'), 
                    platform='android',
                    from_bot_menu=True,
                    url='https://www.okx.com/mini-app/racer'
                ))
                auth_url = web_view.url
                token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                session.headers['x-telegram-init-data'] = token
                await asyncio.sleep(0.7)
                resp = session.get("https://www.okx.com/priapi/v1/affiliate/game/racer/tasks", params=params)
                task = json.loads(resp.text)
                data = task["data"]
                for item in data:
                    if item['id'] == 4:
                        if item["state"] == 0:
                            resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/task", params=params, json={'id': 4})
                            print(resp)
                            text_daily = "\n✅ Собрал ежд. бонус"
                        else:
                            text_daily = ""
                total_play = 0
                total_win = 0
                total_points = 0
                data = {"extUserName": str(name), "linkCode": ""}
                try:
                    resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/info", params=params, json=data)
                    resp.raise_for_status()  
                except requests.exceptions.ConnectionError:
                        await asyncio.sleep(5)  
                except requests.exceptions.HTTPError:
                        await asyncio.sleep(5)
                info = resp.json()
                if resp.status_code != 200:
                        await asyncio.sleep(2)
                        continue
                user = info["data"]
                chances = user["numChances"]
                while True:
                    try:
                        if chances == 0: 
                            balance = user["balancePoints"]
                            secondToRefresh = user["secondToRefresh"]
                            Totalchances = user["numChancesTotal"]
                            if boost(session): 
                                await asyncio.sleep(2)
                            else:
                                secondToRefresh = 90 * (Totalchances - 1 - chances) + secondToRefresh
                                if total_win != 0:
                                    print(f'OKX - Done ({name})')
                                    logger(f"{name} OKX-Racer - Бензин закончился.Info: Balance - {balance} Бензин - {chances}/{Totalchances}. Ждать времени - {secondToRefresh}. Выиграл - {total_win}/{total_play}")
                                await asyncio.sleep(secondToRefresh)
                                break
                        num = random.randint(0, 1)
                        data = {"predict": str(num)}  
                        try:
                            resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/assess", params=params, json=data)
                            if resp.status_code != 200:
                                await asyncio.sleep(5)
                                continue
                        except requests.exceptions.ConnectionError as e:
                            await asyncio.sleep(10)
                            continue
                        info = resp.json()  
                        user = info["data"]
                        error_code = info["error_code"]
                        if error_code != "0":
                            await asyncio.sleep(3)
                            print('err')
                            continue
                        win = user["won"]
                        if win:
                            total_win += 1
                            total_play += 1
                            beet = user["basePoint"]
                            multiplier = user["multiplier"]
                            total_points += beet * multiplier
                            chances = user["numChance"]
                        else:
                            total_play += 1
                            chances = user["numChance"]
                        if chances == 0:
                            resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/info", params=params, json=data)
                            info = resp.json()  
                            user = info["data"]
                            balance = user["balancePoints"]
                            secondToRefresh = user["secondToRefresh"]
                            Totalchances = user["numChancesTotal"]
                            if boost(session): 
                                await asyncio.sleep(2)
                            else:
                                balance = user["balancePoints"]
                                secondToRefresh = user["secondToRefresh"]
                                Totalchances = user["numChancesTotal"]
                                chances = user["numChances"]
                                if chances == 0:
                                    print('okx - done')
                                    secondToRefresh = 90 * (Totalchances - 1 - chances) + secondToRefresh
                                    logger(f"{name} OKX-Racer - Бензин закончился.Info: Balance - {balance} Бензин - {chances}/{Totalchances}. Ждать времени - {secondToRefresh}. Выиграл - {total_win}/{total_play}")
                                    await asyncio.sleep(secondToRefresh)
                                    break
                        wait_time = round(random.uniform(7.8, 8.8), 2)
                        await asyncio.sleep(wait_time)
                    except Exception as e:
                        print(e, {user_id})
                        break
                    
            else:
                break
        else:
            print('satop')
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_okx'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)


async def okx_race(session, message, name, num):
    if num == 1:
         your_beet = "moon"
    else:
         your_beet = "doom"
    timestamp = round(time.time() * 1000)
    data = {"extUserName":str({name}),"linkCode":""}
    params = {"t": timestamp}
    resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/info", params=params, json=data)
    info = json.loads(resp.text)
    user = info["data"]
    Totalchances = user["numChancesTotal"]
    chances = user["numChances"]
    if chances == "0":
        await message.edit_text("❌ Недостаточно бензина!")
    params = {"t": timestamp}
    data = {"predict": str(num)}
    resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/assess", params=params, json=data)
    info = json.loads(resp.text)
    user = info["data"]
    error_code = info["error_code"]
    if error_code != "0":
        await message.edit_text("❌ Ошибка! Попробуйте снова")
        return
    Chances = user["numChance"]
    win = user["won"]
    balance = user["balancePoints"]
    beet = user["basePoint"]
    multiplier = user["multiplier"]
    secondToRefresh = user["secondToRefresh"]
    if str(secondToRefresh) == "-1":
        secondToRefresh = "Энергия полностью восстановлена!"
    else:
        secondToRefresh = 90 * (Totalchances - 1 - Chances) + secondToRefresh
    curCombo = user["curCombo"]
    changeRate = user["changeRate"]
    nowprice = user["currentPrice"]
    oldprice = user["prevPrice"]
    if float(changeRate) < 0:
        emj = "<emoji id=5447183459602669338>📉</emoji>"
    else:
        emj = "<emoji id=5449683594425410231>📈</emoji>"
    if win:
        beet = beet * multiplier
        text = f"{emj} Выпало {your_beet}!\n**<emoji id=5427009714745517609>✅</emoji> Ставка на {your_beet} выиграл +{beet}!**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} Points**\n⛽️ Бензин - {Chances}/{Totalchances}\n<emoji id=5420315771991497307>🔥</emoji> До восстановления бензина - {secondToRefresh} сек\n<emoji id=5438571934210082705>⚡️</emoji> Комбо - {curCombo}\n<emoji id=5472030678633684592>💸</emoji> Прайс: Было - {oldprice} Стало - {nowprice} **({changeRate} %) **"
    else:
        game_res = no_win(your_beet)
        text = f"{emj} Выпало {game_res}!\n**❌ Ставка на {your_beet} проиграл +0({game_res})!**\n<emoji id=5375296873982604963>💰</emoji> Баланс - **{balance} Points**\n⛽️ Бензин - {Chances}/{Totalchances}\n<emoji id=5420315771991497307>🔥</emoji> До восстановления бензина - {secondToRefresh} сек\n<emoji id=5438571934210082705>⚡️</emoji> Комбо - {curCombo}\n<emoji id=5472030678633684592>💸</emoji> Прайс: Было - {oldprice} Стало - {nowprice} **({changeRate} %)**"
    await message.edit_text(text)
    with open('global.json', 'r') as f:
            data = json.load(f)  
            if "okx_games" not in data:
                data['okx_games'] = 0
            data['okx_games'] += 1
    with open('global.json', 'w') as f:
            json.dump(data, f)

def no_win(y_beet):
    if y_beet == "moon":
        return "doom"
    else:
        return "moon"
    
@Client.on_message(filters.command(["aokx", "autookx"], prefixes=pref_p)& filters.me)
async def aokx(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_okx" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_okx']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_okx'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"❌ Автомизация сбор OKX RACER - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_okx'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автомизация OKX RACER - включен") 
            asyncio.create_task(auto_okx(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_okx'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"❌ Автомизация сбор OKX RACER - выключен")
    await asyncio.sleep(3)
    await msg.delete()


def boost(session):
    params = {"t": round(time.time() * 1000)}
    resp = session.get("https://www.okx.com/priapi/v1/affiliate/game/racer/boosts", params=params)
    bost = json.loads(resp.text)
    data = bost["data"]
    for item in data:
        if item['id'] == 1:
            if item["curStage"] != 3:
                params = {"t": round(time.time() * 1000)}
                data = {"id": 1} 
                session.headers['Referer'] = "https://www.okx.com/mini-app/racer/tasks"
                resp = session.post("https://www.okx.com/priapi/v1/affiliate/game/racer/boost", json=data, params=params)
                return True
    return False