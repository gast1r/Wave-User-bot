from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import json
from promo_key.games import games
from utils.agents import get_UA
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
from urllib.parse import unquote
from datetime import datetime,  timedelta, timezone
import random as rnd
import time
import asyncio
import base64, hashlib
import os


@Client.on_message(filters.command(["хамстер", "hamster"], prefixes=pref_p)& filters.me)
async def hamstercombat(client, message):
    try:
        user_id = str((await client.get_me()).id)
        session = requests.Session()
        web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('hamster_kombat_bot'),
            bot=await client.resolve_peer('hamster_kombat_bot'),
            platform='android',
            from_bot_menu=False,
            url='https://hamsterkombat.io/clicker'
        ))
        auth_url = web_view.url
        session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
        payload = {
            "initDataRaw": unquote(auth_url).split('tgWebAppData=')[1].split('&tgWebAppVersion')[0],
            "fingerprint": {}
        }
        try:
            with open('users.json', 'r') as f:
                data = json.load(f)
                date = data[user_id]['hamster_date']
                token = data[user_id]['hamster_token']
        except:
            date = None
        if date == None or datetime.now().strftime("%Y-%m-%d %H:%M:%S") > date:
            try:
                response = requests.post('https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp',json=payload).json()
                token = response['authToken']
                token_expiration = datetime.now() + timedelta(minutes=30)
                with open('users.json', 'r') as f:
                    data = json.load(f)
                    data[user_id]['hamster_token'] = token
                    data[user_id]['hamster_date'] = token_expiration.strftime("%Y-%m-%d %H:%M:%S")
                with open('users.json', 'w') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                await message.edit_text(f"Запустите заново! {e}")
                return
    except:
        await message.edit_text(f"Кажется вы еще не зарегистрировались в Hamster Combat @hamster_kombat_bot")
        return
    session.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-language": "en-US,en;q=0.9,fa;q=0.8",
            "Authorization": f"Bearer",
            "Content-Length": "0",
            "Origin": "https://hamsterkombatgame.io",
            "Priority": "u=0, i",
            "Referer": "https://hamsterkombatgame.io/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', 
            "sec-ch-ua-mobile": "?1", 
            "sec-ch-ua-platform": '"Android"', 
            "Sec-Fetch-Dest": "empty", 
            "Sec-Fetch-Mode": "cors", 
            "Sec-Fetch-Site": "cross-site", 
            "User-Agent": get_UA(user_id)
        }
    session.headers["Authorization"] = f"Bearer {token}"
    resp = session.post('https://api.hamsterkombatgame.io/auth/account-info')
    info = json.loads(resp.text)
    resp = session.post("https://api.hamsterkombatgame.io/clicker/sync")
    info = json.loads(resp.text)
    earn_pas_hour = info['clickerUser']['earnPassivePerHour']
    earn_pas_sec = round(info['clickerUser']['earnPassivePerSec'])
    earn_total = round(info['clickerUser']['totalCoins'])
    balance = round(info['clickerUser']['balanceCoins'])
    balance_st = format_large_number(balance)
    eph_st = format_large_number(earn_pas_hour)
    et_st = format_large_number(earn_total)
    taps = info['clickerUser']['availableTaps']
    one_tap = info['clickerUser']['earnPerTap']
    maxtaps = info['clickerUser']['maxTaps']
    streak = info['clickerUser']['tasks']['streak_days']['days']
    total_keys = info['clickerUser']['totalKeys']
    claim_daily_date = info['clickerUser']['tasks']['streak_days']['completedAt']
    all_upgrades = info['clickerUser']['upgrades']
    resp = session.post("https://api.hamsterkombatgame.io/clicker/config")
    conf = json.loads(resp.text)
    cipher = conf['dailyCipher']['cipher']
    claim_cipher = conf['dailyCipher']['isClaimed']
    tiles = conf['dailyKeysMiniGames']['Tiles']
    candles = conf['dailyKeysMiniGames']['Candles']
    claim_candles = candles['isClaimed']
    seconds_to_next_attempt = candles['remainSecondsToNextAttempt']
    start_date = candles['startDate']
    mini_game_id = candles['id']
    if not claim_candles and seconds_to_next_attempt <= 0:
        game_sleep_time = rnd.randint(10, 30)
        encoded_body = await get_mini_game_cipher(
            user_id=user_id,
            start_date=start_date,
            mini_game_id=mini_game_id,
            score=0
        )
        if encoded_body:
            session.post('https://api.hamsterkombatgame.io/clicker/start-keys-minigame', {'miniGameId': mini_game_id})
            await asyncio.sleep(game_sleep_time)
            resp = session.post('https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame', {'cipher': encoded_body, 'miniGameId': mini_game_id})
            info = json.loads(resp.text)
    claim_tiles = tiles['isClaimed']
    seconds_to_next_attempt = tiles['remainSecondsToNextAttempt']
    start_date = tiles['startDate']
    mini_game_id = tiles['id']
    remain_points = tiles['remainPoints']
    max_points = tiles['maxPoints']
    if not claim_tiles and remain_points > 0:
        game_score = 6000
        if game_score > remain_points:
                    game_score = remain_points
        encoded_body = await get_mini_game_cipher(
        user_id=user_id,
        start_date=start_date,
        mini_game_id=mini_game_id,
        score=game_score
        )
        if encoded_body:
            balance = asyncio.create_task(game_tiles(session, mini_game_id, encoded_body))
    text = ""
    resp = session.post("https://api.hamsterkombatgame.io/clicker/get-promos")
    promo_info = json.loads(resp.text)
    all_promo = promo_info['promos']
    games_pr =  promo_info['states']
    if len(all_promo) > len(games_pr):
        missing_in_promos = []
        for promo in all_promo:
            found = False
            for state in games_pr:
                if promo['promoId'] == state['promoId']:
                    found = True
                    break
            if not found:
                missing_in_promos.append(promo['promoId'])
    if missing_in_promos != []:
        miss_promo_index = 0
    for game_pr in games_pr:
        if game_pr['receiveKeysToday'] < 4:
            promo = game_pr['promoId']
            for game in games:
                if game["promo_id"] == None:
                    pass
                if game["promo_id"] == promo:
                    if os.path.exists(game["keys_file"]):
                        await process_game(game["name"], game["keys_file"], session)
                    else:
                        print(f"Файл с ключами {game['keys_file']} не найден.")
                elif miss_promo_index < len(missing_in_promos) and missing_in_promos[miss_promo_index] == game['promo_id']: 
                    if os.path.exists(game["keys_file"]):
                        await process_game(game["name"], game["keys_file"], session)
                        miss_promo_index += 1
                    else:
                        print(f"Файл с ключами {game['keys_file']} не найден.")
    session.headers.pop("Content-type", None)
    session.headers["Content-Length"] = "0"
    session.headers["Accept"] = "*/*"
    if claim_cipher == False:
        decoded_cipher = decode_cipher(cipher=cipher)
        data = {"cipher": decoded_cipher}
        resp = session.post("https://api.hamsterkombatgame.io/clicker/claim-daily-cipher", json=data)
        text += "\n<emoji id=5427009714745517609>✅</emoji> Разгадал шифр"
    datetime_object = datetime.fromisoformat(claim_daily_date[:-1])
    now_date = datetime.today().strftime('%Y-%m-%d %H.%M.%S')
    if datetime_object != now_date:
        await asyncio.sleep(1)
        resp = session.post("https://api.hamsterkombatgame.io/clicker/list-tasks")
        tasks = json.loads(resp.text)
        for task in tasks['tasks']:
            if task['id'] == 'streak_days' and task['isCompleted'] == False:
                payload = {"taskId": 'streak_days'}
                session.post("https://api.hamsterkombatgame.io/clicker/check-task", json=payload)
                text += f"\n<emoji id=5427009714745517609>✅</emoji> Собрал ежд. бонус (Стрик - {streak})"
            elif task['isCompleted'] == False:
                no_complete = task['id']
                if no_complete != None:
                    payload = {"taskId": no_complete}
                session.post("https://api.hamsterkombatgame.io/clicker/check-task", json=payload)
                text += "\n<emoji id=5427009714745517609>✅</emoji> Выполнил задание"
    resp = session.post("https://api.hamsterkombatgame.io/clicker/boosts-for-buy")
    info = json.loads(resp.text)
    resp = session.post("https://api.hamsterkombatgame.io/clicker/config")
    info = json.loads(resp.text)
    session.headers["Accept"] = "application/json"
    session.headers["Content-Length"] = "56"
    session.headers['Content-type'] = "application/json"
    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Hamster Combat\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance_st}\n<emoji id=5420315771991497307>🔥</emoji>Энергии - {taps}/{maxtaps}\n<emoji id=5472030678633684592>💸</emoji> Заработок в час - {eph_st}\n<emoji id=5472030678633684592>💸</emoji> Заработок в сек - {earn_pas_sec}\n<emoji id=5409048419211682843>💵</emoji> Зарабатано всего - {et_st}\n🔑 Ключей - {total_keys}\n<emoji id=5469718869536940860>👆</emoji> Тапаю хомячка...{text}")
    while True:
        if taps == None:
            await asyncio.sleep(3)
            resp = session.post("https://api.hamsterkombatgame.io/clicker/sync")
            info = json.loads(resp.text)
            taps = info['clickerUser']['availableTaps']
        if taps < 30 and taps == 0:
            await asyncio.sleep(2)
            taps = fullenergy(session, session.headers)
        if taps == -1:
            await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Hamster Combat\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance_st}\n<emoji id=5420315771991497307>🔥</emoji>Энергии - {taps}\n<emoji id=5472030678633684592>💸</emoji> Заработок в час - {eph_st}\n<emoji id=5472030678633684592>💸</emoji> Заработок в сек - {earn_pas_sec}\n<emoji id=5409048419211682843>💵</emoji> Зарабатано всего - {et_st}\n🔑 Ключей - {total_keys}\n Problem...{text}")
            break
        if taps == -2:
            taps = 0
            await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Hamster Combat\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance_st}\n<emoji id=5420315771991497307>🔥</emoji>Энергии - {taps}\n<emoji id=5472030678633684592>💸</emoji> Заработок в час - {eph_st}\n<emoji id=5472030678633684592>💸</emoji> Заработок в сек - {earn_pas_sec}\n<emoji id=5409048419211682843>💵</emoji> Зарабатано всего - {et_st}\n🔑 Ключей - {total_keys}\n<emoji id=5431449001532594346>⚡️</emoji> Энергия полностью потрачена (cooldown){text}")
            break
        else:
            taps = taptap(session, taps)

def decode_cipher(cipher: str):
    encoded = cipher[:3] + cipher[4:]
    return base64.b64decode(encoded).decode('utf-8')


def taptap(session, taps):
    total_taps = 0
    while taps > 61:
        clicks = rnd.randint(150, 250)
        total_taps += clicks
        payload = {"count": clicks, "availableTaps": taps, "timestamp": round(time.time() * 1000)}
        resp = session.post("https://api.hamsterkombatgame.io/clicker/tap", json=payload)
        if resp.status_code != 400 and resp.status_code != 200:
            return -1
        user = json.loads(resp.text)
        taps = user['clickerUser']['availableTaps']
        total_keys = user['clickerUser']['totalKeys']
        time.sleep(2)
        return taps

def fullenergy(session, headers):
    headers.pop("Content-type", None)
    headers["Content-Length"] = "0"
    headers["Accept"] = "*/*"
    resp = session.post("https://api.hamsterkombatgame.io/clicker/boosts-for-buy")
    info = json.loads(resp.text)
    id = info['boostsForBuy'][2]["id"]
    used = info['boostsForBuy'][2]["level"]
    cooldown = info['boostsForBuy'][2]['cooldownSeconds']
    if used <= 6 and cooldown == 0:
        payload = {"boostId": id, "timestamp": round(time.time() * 1000)}
        headers["Accept"] = "application/json"
        headers["Content-Length"] = "56"
        headers['Content-type'] = "application/json"
        resp = session.post("https://api.hamsterkombatgame.io/clicker/buy-boost", json=payload)
        headers.pop("Content-type", None)
        headers["Content-Length"] = "0"
        headers["Accept"] = "*/*"
        resp = session.post("https://api.hamsterkombatgame.io/clicker/sync")
        info = json.loads(resp.text)
        taps = info['clickerUser']['availableTaps']
        return taps
    else:
        return -2

def find_best_upgrades(upgrades, time_horizon=2):
        best_upgrades = []
        for upgrade in upgrades:
            if upgrade['isAvailable'] and not upgrade['isExpired']:
                try:
                    hours_to_recoup = upgrade['price'] / (upgrade['profitPerHourDelta'])
                except:
                    continue
                if hours_to_recoup <= time_horizon * 24:
                    x_day_return = upgrade['profitPerHourDelta'] * 24 * time_horizon
                    upgrade['x_day_return'] = x_day_return - upgrade['price']
                    best_upgrades.append(upgrade)
        best_upgrades.sort(key=lambda upgrade: upgrade['x_day_return'], reverse=True)
        return best_upgrades[:3]


@Client.on_message(filters.command(["ahamster", "ахомяк"], prefixes=pref_p)& filters.me)
async def hamstergee_auto(client, message):
    with open('users.json', 'r') as f:
            data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_ham" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_ham']
        if auto:
            data[user_id]['auto_ham'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text("❌ Автоматимизация Hamster - выключен") 
        else:
            data[user_id]['auto_ham'] = True
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text("<emoji id=5427009714745517609>✅</emoji> Автоматимизация Hamster - включен") 
            asyncio.create_task(automatic_hamster(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_ham'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Автоматимизация Hamster - выключен")
    await asyncio.sleep(3)
    await msg.delete()


async def automatic_hamster(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
        if user_id in data and "auto_ham" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_ham']
            if auto:
                try:
                    web_view = await client.invoke(RequestWebView(
                    peer=await client.resolve_peer('hamster_kombat_bot'),
                    bot=await client.resolve_peer('hamster_kombat_bot'),
                    platform='android',
                    from_bot_menu=False,
                    url='https://hamsterkombat.io/clicker'
                ))
                    auth_url = web_view.url
                    payload = {
                        "initDataRaw": unquote(auth_url).split('tgWebAppData=')[1].split('&tgWebAppVersion')[0],
                        "fingerprint": {}
                    }
                except:
                    break
                try:
                    with open('users.json', 'r') as f:
                        data = json.load(f)
                        date = data[user_id]['hamster_date']
                        token = data[user_id]['hamster_token']
                except:
                    date = None
                await asyncio.sleep(4)
                if date == None or datetime.now().strftime("%Y-%m-%d %H:%M:%S") > date:
                    try:
                        response = requests.post('https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp',json=payload).json()
                        token = response['authToken']
                        
                        token_expiration = datetime.now() + timedelta(minutes=30)
                        with open('users.json', 'r') as f:
                            data = json.load(f)
                            data[user_id]['hamster_token'] = token
                            data[user_id]['hamster_date'] = token_expiration.strftime("%Y-%m-%d %H:%M:%S")
                        with open('users.json', 'w') as f:
                            json.dump(data, f, indent=2)
                    except Exception as e:
                        print('Err hamster')
                        break
                else:
                    session = requests.Session()
                    session.proxies = {
                        "http": f"https://{GET_PROXY(user_id)}"
                    }
                    text = ""
                    session.headers = {
                            "Accept": "*/*",
                            "Accept-Encoding": "gzip, deflate, br, zstd",
                            "Accept-language": "en-US,en;q=0.9,fa;q=0.8",
                            "Authorization": f"Bearer",
                            "Content-Length": "0",
                            "Origin": "https://hamsterkombatgame.io",
                            "Priority": "u=0, i",
                            "Referer": "https://hamsterkombatgame.io/",
                            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', 
                            "sec-ch-ua-mobile": "?1", 
                            "sec-ch-ua-platform": '"Android"', 
                            "Sec-Fetch-Dest": "empty", 
                            "Sec-Fetch-Mode": "cors", 
                            "Sec-Fetch-Site": "cross-site", 
                            "User-Agent": get_UA(user_id)
                        }
                    session.headers["Authorization"] = f"Bearer {token}"
                    resp = session.post("https://api.hamsterkombatgame.io/clicker/sync")
                    err_text = f"{resp}  {resp.text}"
                    info = json.loads(resp.text)
                    balance = round(info['clickerUser']['balanceCoins'])
                    taps = info['clickerUser']['availableTaps']
                    one_tap = info['clickerUser']['earnPerTap']
                    streak = info['clickerUser']['tasks']['streak_days']['days']
                    claim_daily_date = info['clickerUser']['tasks']['streak_days']['completedAt']
                    resp = session.post("https://api.hamsterkombatgame.io/clicker/config")
                    conf = json.loads(resp.text)
                    cipher = conf['dailyCipher']['cipher']
                    claim_cipher = conf['dailyCipher']['isClaimed']
                    claim_minigame = conf['dailyKeysMiniGames']['Candles']['isClaimed']
                    text = ""
                    resp = session.post("https://api.hamsterkombatgame.io/clicker/get-promos")
                    promo_info = json.loads(resp.text)
                    all_promo = promo_info['promos']
                    games_pr =  promo_info['states']
                    if len(all_promo) > len(games_pr):
                        missing_in_promos = []
                        for promo in all_promo:
                            found = False
                            for state in games_pr:
                                if promo['promoId'] == state['promoId']:
                                    found = True
                                    break
                            if not found:
                                missing_in_promos.append(promo['promoId'])
                    if missing_in_promos != []:
                        for promo in missing_in_promos:
                            miss_promo = promo
                    for game_pr in games_pr:
                        if game_pr['receiveKeysToday'] < 4 or game_pr['receiveKeysToday'] < 8 and game_pr['promoId'] == '112887b0-a8af-4eb2-ac63-d82df78283d9':
                            promo = game_pr['promoId']
                            print(f'Найдена непройденная игра! - {promo}')
                            for game in games:
                                if game["promo_id"] == None:
                                    pass
                                if game["promo_id"] == promo:
                                    if os.path.exists(game["keys_file"]):
                                        await process_game(game["name"], game["keys_file"], session)
                                    else:
                                        print(f"Файл с ключами {game['keys_file']} не найден.")
                                elif miss_promo != None and miss_promo == game['promo_id']: 
                                    print(f"Игра с promo_id {promo} не найдена в списке игр states.")
                                    if os.path.exists(game["keys_file"]):
                                        await process_game(game["name"], game["keys_file"], session)
                                    else:
                                        print(f"Файл с ключами {game['keys_file']} не найден.")
                    await asyncio.sleep(2)
                    session.headers.pop("Content-type", None)
                    session.headers["Content-Length"] = "0"
                    session.headers["Accept"] = "*/*"
                    if claim_cipher == False:
                        decoded_cipher = decode_cipher(cipher=cipher)
                        data = {"cipher": decoded_cipher}
                        resp = session.post("https://api.hamsterkombatgame.io/clicker/claim-daily-cipher", json=data)
                        text += " Разгадал шифр"
                    claim_cipher = conf['dailyCipher']['isClaimed']
                    candles = conf['dailyKeysMiniGames']['Candles']
                    tiles = conf['dailyKeysMiniGames']['Tiles']
                    claim_candles = candles['isClaimed']
                    seconds_to_next_attempt = candles['remainSecondsToNextAttempt']
                    start_date = candles['startDate']
                    mini_game_id = candles['id']
                    if not claim_candles and seconds_to_next_attempt <= 0:
                        game_sleep_time = rnd.randint(12, 26)
                        encoded_body = await get_mini_game_cipher(
                            user_id=user_id,
                            start_date=start_date,
                            mini_game_id=mini_game_id,
                            score=0
                        )
                        if encoded_body:
                            session.post('https://api.hamsterkombatgame.io/clicker/start-keys-minigame', {'miniGameId': mini_game_id})
                            await asyncio.sleep(game_sleep_time)
                            resp = session.post('https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame', {'cipher': encoded_body, 'miniGameId': mini_game_id})
                            info = json.loads(resp.text)
                            total_keys = info['clickerUser']['totalKeys']
                    claim_tiles = tiles['isClaimed']
                    seconds_to_next_attempt = tiles['remainSecondsToNextAttempt']
                    start_date = tiles['startDate']
                    mini_game_id = tiles['id']
                    remain_points = tiles['remainPoints']
                    max_points = tiles['maxPoints']
                    if not claim_tiles and remain_points > 0:
                        game_score = 6000
                        if game_score > remain_points:
                                    game_score = remain_points
                        encoded_body = await get_mini_game_cipher(
                        user_id=user_id,
                        start_date=start_date,
                        mini_game_id=mini_game_id,
                        score=game_score
                        )
                        if encoded_body:
                            balance = await game_tiles(session, mini_game_id, encoded_body)
                    claim_cipher = conf['dailyCipher']['isClaimed']
                    candles = conf['dailyKeysMiniGames']['Candles']
                    claim_candles = candles['isClaimed']
                    seconds_to_next_attempt = candles['remainSecondsToNextAttempt']
                    start_date = candles['startDate']
                    mini_game_id = candles['id']
                    datetime_object = datetime.fromisoformat(claim_daily_date[:-1])
                    now_date = datetime.today().strftime('%Y-%m-%d %H.%M.%S')
                    if datetime_object != now_date:
                        await asyncio.sleep(1)
                        resp = session.post("https://api.hamsterkombatgame.io/clicker/list-tasks")
                        tasks = json.loads(resp.text)
                        for task in tasks['tasks']:
                            if task['id'] == 'streak_days' and task['isCompleted'] == False:
                                payload = {"taskId": 'streak_days'}
                                session.post("https://api.hamsterkombatgame.io/clicker/check-task", json=payload)
                                text += f"Собрал ежд. бонус (Стрик - {streak})"
                            elif task['isCompleted'] == False:
                                no_complete = task['id']
                                if no_complete != None:
                                    payload = {"taskId": no_complete}
                                session.post("https://api.hamsterkombatgame.io/clicker/check-task", json=payload)
                                text += " Выполнил задание"
                    resp = session.post("https://api.hamsterkombatgame.io/clicker/boosts-for-buy")
                    info = json.loads(resp.text)
                    resp = session.post("https://api.hamsterkombatgame.io/clicker/config")
                    info = json.loads(resp.text)
                    session.headers["Accept"] = "application/json"
                    session.headers["Content-Length"] = "56"
                    session.headers['Content-type'] = "application/json"
                    while True:
                        if taps == None:
                            await asyncio.sleep(4)
                            taps = taptap(session, taps)
                            continue
                        if taps < 30 and taps == 0:
                            await asyncio.sleep(2)
                            taps = fullenergy(session, session.headers)
                        if taps == -1:
                            break
                        if taps == -2:
                            taps = 0
                            print(f'Hamster - Done ({user_name})')
                            balance = format_large_number(balance)
                            logger(f"{user_name} | Hamster - (cooldown). Info: Balance - {balance} Energy - {taps} | {text}")
                            await asyncio.sleep(1980 + rnd.randint(10, 120))
                            break
                        else:
                            taps = taptap(session, taps)
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_ham'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)

async def game_tiles(session, mini_game_id, encoded_body):
    session.post('https://api.hamsterkombatgame.io/clicker/start-keys-minigame', {'miniGameId': mini_game_id})
    await asyncio.sleep(60)
    resp = session.post('https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame', {'cipher': encoded_body, 'miniGameId': mini_game_id})
    info = json.loads(resp.text)
    balance = round(info['clickerUser']['balanceCoins'])
    await asyncio.sleep(2)
    return balance


async def process_game(game_name, keys_file, session):
    try:
        ien = 1
        with open(keys_file, 'r') as file:
            lines = file.readlines() 
        if 0 <= ien - 1 < len(lines):
            key = lines[ien - 1].strip()
        while key:
            await asyncio.sleep(1)
            payload = {"promoCode": key}
            response = session.post('https://api.hamsterkombatgame.io/clicker/apply-promo', json=payload)
            if response.status_code == 200:
                del lines[ien - 1]
                with open(keys_file, 'w') as file:
                    file.writelines(lines)
                with open(keys_file, 'r') as file:
                    lines = file.readlines() 
                    if 0 <= ien - 1 < len(lines):
                        key = lines[ien - 1].strip()
            elif "MaxKeysReceived" in response.text: 
                break 
            elif "InvalidPromoCode" in response.text:
                    del lines[ien - 1]
                    with open(keys_file, 'w') as file:
                        file.writelines(lines)
                    with open(keys_file, 'r') as file:
                        lines = file.readlines() 
                    if 0 <= ien - 1 < len(lines):
                        key = lines[ien - 1].strip()
    except:
        pass

def format_large_number(num):
    if num >= 10**100:  # 1 googl
        return f"{num / 10**100:.1f}G"
    elif num >= 10**77:  # 1 unvigintillion
        return f"{num / 10**77:.1f}U"
    elif num >= 10**73:  # 1 vigintillion
        return f"{num / 10**73:.1f}V"
    elif num >= 10**69:  # 1 novemdecillion
        return f"{num / 10**69:.1f}Nd"
    elif num >= 10**65:  # 1 octodecillion
        return f"{num / 10**65:.1f}O"  
    elif num >= 10**61:  # 1 septendecillion
        return f"{num / 10**61:.1f}Sp"
    elif num >= 10**57:  # 1 sexdecillion
        return f"{num / 10**57:.1f}SX"
    elif num >= 10**53:  # 1 quindecillion
        return f"{num / 10**53:.1f}QI"
    elif num >= 10**49:  # 1 quattuordecillion
        return f"{num / 10**49:.1f}QD"
    elif num >= 10**45:  # 1 tredecillion
        return f"{num / 10**45:.1f}TD"
    elif num >= 10**33:  # 1 undecillion
        return f"{num / 10**33:.1f}U"
    elif num >= 1_000_000_000_000_000_000_000_000_000_000_000:  # 1 decillion
        return f"{num / 1_000_000_000_000_000_000_000_000_000_000_000:.1f}D"
    elif num >= 1_000_000_000_000_000_000_000_000_000_000:  # 1 nonillion
        return f"{num / 1_000_000_000_000_000_000_000_000_000_000:.1f}n"
    elif num >= 1_000_000_000_000_000_000_000_000_000:  # 1 octillion
        return f"{num / 1_000_000_000_000_000_000_000_000_000:.1f}O"
    elif num >= 1_000_000_000_000_000_000_000_000:  # 1 septillion
        return f"{num / 1_000_000_000_000_000_000_000_000:.1f}Sp"
    elif num >= 1_000_000_000_000_000_000_000:  # 1 sextilion
        return f"{num / 1_000_000_000_000_000_000_000:.1f}Sx"
    elif num >= 1_000_000_000_000_000_000:  # 1 квинтилион
        return f"{num / 1_000_000_000_000_000_000:.1f}Qi"
    elif num >= 1_000_000_000_000_000:  # 1 квадрилион
        return f"{num / 1_000_000_000_000_000:.1f}Q"
    elif num >= 1_000_000_000_000:  # 1 трилион
        return f"{num / 1_000_000_000_000:.1f}T"
    elif num >= 1_000_000_000:  # 1 миллиард
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:  # 1 миллион
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1000:  # 1 тысяча
        return f"{num / 1000:.1f}K"
    return str(num)


async def get_mini_game_cipher(user_id: int,
                               start_date: str,
                               mini_game_id: str,
                               score: int):
    secret1 = "R1cHard_AnA1"
    secret2 = "G1ve_Me_y0u7_Pa55w0rD"

    start_dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    start_number = int(start_dt.replace(tzinfo=timezone.utc).timestamp())
    cipher_score = (start_number + score) * 2

    combined_string = f'{secret1}{cipher_score}{secret2}'

    sig = hashlib.sha256(combined_string.encode()).digest()
    sig = base64.b64encode(sig).decode()

    game_cipher = await get_game_cipher(start_number=start_number)

    data = f'{game_cipher}|{user_id}|{mini_game_id}|{cipher_score}|{sig}'

    encoded_data = base64.b64encode(data.encode()).decode()

    return encoded_data

async def get_game_cipher(start_number: str):
    magic_index = int(start_number % (len(str(start_number)) - 2))
    res = ""
    for i in range(len(str(start_number))):
        res += '0' if i == magic_index else str(int(rnd.random() * 10))
    return res