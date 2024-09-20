from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
from utils.agents import get_UA
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
import random, hashlib, json, math, re
import datetime as dt
import time


@Client.on_message(filters.command(["elon", "илон"], prefixes=pref_p)& filters.me)
async def elon(client, message):
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
            "Api-Key": "empty",
            "Api-Time": f"{round(time.time())}",
            "Cache-Control": "no-chache",
            "Content-Length": "508",
            "Content-Type": "application/json",
            "Is-Beta-Server": "null",
            "Origin": "https://game.xempire.io",
            "Pragma": "no-chache",
            "Priority": "u=1, i",
            "Referer": "https://game.xempire.io/",
            'Host': 'api.xempire.io',
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": get_UA(user_id)
        })
    web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('@empirebot'),
            bot=await client.resolve_peer('@empirebot'), 
            platform='android',
            from_bot_menu=True,
            url='https://game.xempire.io'
        ))
    auth_url = web_view.url
    token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
    key = token.split('&hash=')[1]
    data = {
    "data":{"initData":f"{token}","platform":"android","chatId":"","chatType":"sender","chatInstance":"-179314549733246004"}
    }
    response = session.post('https://api.xempire.io/telegram/auth', json=data)
    session.headers['Api-Key'] = str(key)
    if response.status_code == 200:
        text = ""
        await set_sign_headers({}, session)
        resp = session.post('https://api.xempire.io/user/data/all', json={})
        full = json.loads(resp.text)
        user = full['data']['hero']
        db = full['data']['dbData']
        quests = db['dbQuests']
        level = user['level']
        balance = user['money']
        bal_st = format_large_number(balance)
        moneyPH = user['moneyPerHour']
        MPH_st = format_large_number(moneyPH)
        exp = user['exp']
        exp_st = format_large_number(exp)
        per_tap = user['earns']['task']['moneyPerTap']
        limit = user['earns']['task']['limit']
        energy = user['earns']['task']['energy']
        energy_recovery = user['earns']['task']['recoveryPerSecond']
        time_recovery = (limit - energy) / energy_recovery
        eng_st = format_large_number(energy)
        limit_st = format_large_number(limit)
        moneyPS = round(moneyPH / 60 / 60)
        MPS_st = format_large_number(moneyPS)
        offline_bonus = int(user['offlineBonus'])
        resp = session.post('https://api.xempire.io/user/data/after', json={})
        profile = json.loads(resp.text)
        daily_rewards = profile['data']['dailyRewards']
        rewards = profile['data']['quests']
        for item in db["dbQuests"]:
            if "rebus_" in item['key']:
                task_type = "rebus"
                task_key = item['key']
                task_ans = item['checkData']
                await checker_rebus_and_riddle(session, rewards, task_key, task_ans)
            elif "riddle_" in item['key']:
                task_type = "riddle"
                task_key = item['key']
                task_ans = item['checkData']
                await checker_rebus_and_riddle(session, rewards, task_key, task_ans)
        day_claim = None
        for day, status in daily_rewards.items():
            if status == 'canTake':
                day_claim = day
                break
        if day_claim is not None:
             await set_sign_headers({'data': f"{day_claim}"}, session)
             resp = session.post('https://api.xempire.io/quests/daily/claim', json={'data': f"{day_claim}"})
             text += f"\n<emoji id=5427009714745517609>✅</emoji> Ежд. бонус собран"
        if offline_bonus > moneyPH:
            await set_sign_headers({}, session)
            resp = session.post('https://api.xempire.io/hero/bonus/offline/claim', json={})
            offline_st = format_large_number(offline_bonus)
            text += f"\n<emoji id=5427009714745517609>✅</emoji> Оффлайн майнинг собран +{offline_st}"
            await set_sign_headers({}, session)
            resp = session.post('https://api.xempire.io/user/data/all', json={})
            full = json.loads(resp.text)
            balance = user['money']
            bal_st = format_large_number(balance)
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - X-Empire\n<emoji id=5375296873982604963>💰</emoji> Баланс - {bal_st}\n🆙 Уровень - {level}\n<emoji id=5420315771991497307>🔥</emoji>Энергии - {eng_st}/{limit_st}\n<emoji id=5472030678633684592>💸</emoji> Заработок в час - {MPH_st}\n<emoji id=5472030678633684592>💸</emoji> Заработок в сек - {MPS_st}\n<emoji id=5409048419211682843>💵</emoji> Зарабатано всего - {exp_st}\n<emoji id=5469718869536940860>👆</emoji> Тапаю елона {text}")
        tapper, earned_money_sum = await perform_taps(per_tap, energy, session)
        text += await daily_quests(session)
        if tapper == "done":
            resp = session.post('https://api.xempire.io/user/data/all', json={})
            full = json.loads(resp.text)
            balance = user['money']
            limit = user['earns']['task']['limit']
            energy = user['earns']['task']['energy']
            energy_recovery = user['earns']['task']['recoveryPerSecond']
            time_recovery = (limit - energy) / energy_recovery
            bal_st = format_large_number(balance)
            eng_st = format_large_number(energy)
            time_rec = time.strftime("%M:%S", time.gmtime(time_recovery))
            earned_money_sum_st = format_large_number(earned_money_sum)
            await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - X-Empire\n<emoji id=5375296873982604963>💰</emoji> Баланс - {bal_st}\n🆙 Уровень - {level}\n<emoji id=5420315771991497307>🔥</emoji>Энергии - {eng_st}/{limit_st}\n<emoji id=5472030678633684592>💸</emoji> Заработок в час - {MPH_st}\n<emoji id=5472030678633684592>💸</emoji> Заработок в сек - {MPS_st}\n<emoji id=5409048419211682843>💵</emoji> Зарабатано всего - {exp_st}\n<emoji id=5431449001532594346>⚡️</emoji> Энергия закончилась\n<emoji id=5472030678633684592>💸</emoji> Заработал +{earned_money_sum_st}\n<emoji id=5431449001532594346>⚡️</emoji> До восстановление Энергии: {time_rec}{text}")
    else:
        print("Ошибка:", response.status_code, response.text)


async def daily_quests(session) -> None:
        json_data = {}
        await set_sign_headers(data=json_data, session=session)
        response =  session.post('https://api.xempire.io/quests/daily/progress/all', json=json_data)
        response_json = json.loads(response.text)
        tap_copm = response_json['data']['tap']['isComplete']
        tap_r = response_json['data']['tap']['isRewarded']
        skil_r = response_json['data']['skill_5']['isRewarded']
        skill_copm = response_json['data']['skill_5']['isComplete']
        all_copm = response_json['data']['all_complete']['isComplete']
        all_r = response_json['data']['all_complete']['isRewarded']
        if response_json['data']['youtube'] != None and response_json['data']['youtube']['isRewarded'] != True:
            description = response_json['data']['youtube']['description']
            match = re.search(r"Эпизод (\d+)", description)
            if match:
                episode_number = int(match.group(1))
                episode = f"Episode {episode_number}"
                with open('combo.json', 'r') as f:
                    data = json.load(f)
                    try:
                        code = data['elon'][episode]
                    except:
                        return ""
                    if code != None:
                        payload = {"data":{"quest":"youtube","code": f"{code}"}}
                        await set_sign_headers(data=payload, session=session)
                        await asyncio.sleep(1)
                        resp = session.post('https://api.xempire.io/quests/daily/progress/claim', json=payload)
                        print(resp)
                        print(code)
            else:
                print("Номер эпизода не найден в описании.")
                return ""
        if response_json['data']['youtube_2'] != None and response_json['data']['youtube_2']['isRewarded'] != True:
            description = response_json['data']['youtube_2']['description']
            match = re.search(r"Эпизод (\d+)", description)
            if match:
                episode_number = int(match.group(1))
                episode = f"Episode {episode_number}"
                with open('combo.json', 'r') as f:
                    data = json.load(f)
                    try:
                        code = data['elon'][episode]
                    except:
                        return ""
                    if code != None:
                        payload = {"data":{"quest":"youtube_2","code": f"{code}"}}
                        await set_sign_headers(data=payload, session=session)
                        await asyncio.sleep(1)
                        resp = session.post('https://api.xempire.io/quests/daily/progress/claim', json=payload)
                        print(resp)
                        print(code)
            else:
                print("Номер эпизода не найден в описании.")
                return ""
            text = ""
        if tap_copm == True and tap_r == False:
            json_data = {"data":{"quest":"tap", "code":"null"}}
            await set_sign_headers(data=json_data, session=session)
            resp = session.post('https://api.xempire.io/quests/daily/progress/claim', json=json_data)
        if skill_copm == True and skil_r == False:
            json_data = {"data":{"quest":"skill_5","code":"null"}}
            await set_sign_headers(data=json_data, session=session)
            session.post('https://api.xempire.io/quests/daily/progress/claim', json=json_data)
        await asyncio.sleep(2)
        response =  session.post('https://api.xempire.io/quests/daily/progress/all', json=json_data)
        response_json = json.loads(response.text)
        tap_copm = response_json['data']['tap']['isComplete']
        tap_r = response_json['data']['tap']['isRewarded']
        skil_r = response_json['data']['skill_5']['isRewarded']
        skill_copm = response_json['data']['skill_5']['isComplete']
        all_copm = response_json['data']['all_complete']['isComplete']
        all_r = response_json['data']['all_complete']['isRewarded']
        if all_copm == True and all_r == False:
            json_data = {"data":{"quest":"all_complete","code":"null"}}
            await set_sign_headers(data=json_data, session=session)
            session.post('https://api.xempire.io/quests/daily/progress/claim', json=json_data)
        return text

async def all_quests(session,quests, client) -> None:
        for quest in quests:
            if quest['needCheck']:
                print(quest['key'])
                if "tg" in quest['key'] and "major" not in quest['key']:
                    print(quest['actionUrl'].split('t.me/')[1])
                    await client.join_chat(quest['actionUrl'].split('t.me/')[1])
                    payload = {"data":[quest['key'],"null"]}
                    await set_sign_headers(data=payload, session=session)
                    resp = session.post('https://api.xempire.io/quests/check', json=payload)
                    print(resp)
                    await asyncio.sleep(5)
                    await client.leave_chat(quest['actionUrl'].split('t.me/')[1])
                elif "wallet" in quest['key'] or "deposit" in quest['key']:
                    pass
                else:
                    payload = {"data":[quest['key'],"null"]}
                    await set_sign_headers(data=payload, session=session)
                    resp = session.post('https://api.xempire.io/quests/check', json=payload)
                    print(resp)
                await asyncio.sleep(3)

async def perform_taps(per_tap, energy, session) -> None:
        earned_money_sum = 0
        while True:
            taps_per_second = 20
            seconds = random.randint(3, 5)
            earned_money = per_tap * taps_per_second * seconds
            earned_money_sum += earned_money
            energy_spent = math.ceil(earned_money / 2)
            energy -= energy_spent
            if energy < 0:
                return "done", earned_money_sum
            await asyncio.sleep(delay=seconds)
            try:
                json_data = {'data': {'data':{'task': {'amount': earned_money, 'currentEnergy': energy}}, 'seconds': seconds}}
                await set_sign_headers(data=json_data, session=session)
                resp = session.post("https://api.xempire.io/hero/action/tap", json=json_data)
                response_json = json.loads(resp.text)
                success = response_json.get('success', False)
                if success:
                     continue
            except Exception as error:
                 print(error)
                 break
             

async def set_sign_headers(data, session): 
    time_string = str(int(time.time()))
    json_string = json.dumps(data)
    hash_object = hashlib.md5()
    hash_object.update(f"{time_string}_{json_string}".encode('utf-8'))
    hash_string = hash_object.hexdigest()
    session.headers['Api-Time'] = time_string
    session.headers['Api-Hash'] = hash_string


async def checker_rebus_and_riddle(session, rewards, task_key, task_ans):
    for reward in rewards:
        if reward['key'] == task_key and reward['isRewarded'] == True:
            return 
    payload = {"data": [task_key, task_ans]}
    await set_sign_headers(payload, session)
    resp = session.post("https://api.xempire.io/quests/check", json=payload)
    if resp.status_code == 200:
        payload = {"data": [task_key, "null"]}
        await set_sign_headers(payload, session)
        resp = session.post("https://api.xempire.io/quests/claim", json=payload)


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


@Client.on_message(filters.command(["aelon", "autoelon", "ааелон"], prefixes=pref_p)& filters.me)
async def elon_auto(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_elon" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_elon']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_elon'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"❌ Автоматический сбор X-Empire - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_elon'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"✅ Автоматический сбор X-Empire - включен") 
            asyncio.create_task(auto_elon(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_elon'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"❌ Автоматический сбор X-Empire - выключен")
    await asyncio.sleep(2)
    await msg.delete()


async def auto_elon(client, user_id, user_name):
  while True:
      with open('users.json', 'r') as f:
          data = json.load(f)
      if user_id in data and "auto_elon" in data[user_id]:
          with open('users.json', 'r') as f:
              data = json.load(f)
              auto = data[user_id]['auto_elon']
          if auto:
            session = requests.Session() 
            try:
                session.proxies = {
                    "http": f"https://{GET_PROXY(user_id)}"
                }
                session.headers.update({
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "Api-Key": "empty",
                "Api-Time": f"{round(time.time() * 1000)}",
                "Cache-Control": "no-chache",
                "Content-Length": "508",
                "Content-Type": "application/json",
                "Is-Beta-Server": "null",
                "Origin": "https://game.xempire.io",
                "Pragma": "no-chache",
                "Priority": "u=1, i",
                "Referer": "https://game.xempire.io/",
                'Host': 'api.xempire.io',
                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": '"Android"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": get_UA(user_id)
                })
                web_view = await client.invoke(RequestWebView(
                    peer=await client.resolve_peer('@empirebot'),
                    bot=await client.resolve_peer('@empirebot'), 
                    platform='android',
                    from_bot_menu=True,
                    url='https://game.xempire.io'
                ))
                auth_url = web_view.url
                token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                key = token.split('&hash=')[1]
                data = {
                "data":{"initData":f"{token}","platform":"android","chatId":"","chatType":"sender","chatInstance":"-179314549733246004"}
                }
                response = session.post('https://api.xempire.io/telegram/auth', json=data)
                session.headers['Api-Key'] = str(key)
                if response.status_code == 200:
                    text = ""
                    await set_sign_headers({}, session)
                    resp = session.post('https://api.xempire.io/user/data/all', json={})
                    full = json.loads(resp.text)
                    user = full['data']['hero']
                    db = full['data']['dbData']
                    per_tap = user['earns']['task']['moneyPerTap']
                    balance = user['money']
                    limit = user['earns']['task']['limit']
                    energy = user['earns']['task']['energy']
                    energy_recovery = user['earns']['task']['recoveryPerSecond']
                    bal_st = format_large_number(balance)
                    offline_bonus = int(user['offlineBonus'])
                    resp = session.post('https://api.xempire.io/user/data/after', json={})
                    profile = json.loads(resp.text)
                    daily_rewards = profile['data']['dailyRewards']
                    rewards = profile['data']['quests']
                    for item in db["dbQuests"]:
                        if "rebus_" in item['key']:
                            task_type = "rebus"
                            task_key = item['key']
                            task_ans = item['checkData']
                            await checker_rebus_and_riddle(session, rewards, task_key, task_ans)
                        elif "riddle_" in item['key']:
                            task_type = "riddle"
                            task_key = item['key']
                            task_ans = item['checkData']
                            await checker_rebus_and_riddle(session, rewards, task_key, task_ans)
                    day_claim = None
                    for day, status in daily_rewards.items():
                        if status == 'canTake':
                            day_claim = day
                            break
                    if day_claim is not None:
                        await set_sign_headers({'data': f"{day_claim}"}, session)
                        resp = session.post('https://api.xempire.io/quests/daily/claim', json={'data': f"{day_claim}"})
                        text += f"Ежд. бонус собран|"
                    if offline_bonus > 0:
                        await set_sign_headers({}, session)
                        resp = session.post('https://api.xempire.io/hero/bonus/offline/claim', json={})
                        offline_st = format_large_number(offline_bonus)
                        text += f"Оффлайн майнинг собран +{offline_st}"
                    tapper, earned_money_sum = await perform_taps(per_tap, energy, session)
                    text += await daily_quests(session)
                    if tapper == "done":
                        resp = session.post('https://api.xempire.io/user/data/all', json={})
                        full = json.loads(resp.text)
                        balance = user['money']
                        limit = user['earns']['task']['limit']
                        energy = user['earns']['task']['energy']
                        energy_recovery = user['earns']['task']['recoveryPerSecond']
                        moneyPH = user['moneyPerHour']
                        MPH_st = format_large_number(moneyPH)
                        bal_st = format_large_number(balance)
                        text += " Потапал елона"
                    logger(f"{user_name} X-empire | Info: Balance - {bal_st} MPH - {MPH_st} Info - {text}")
                    trnd = random.randint(40, 100)
                    print(f'Elon - Done ({user_name})')
                    await asyncio.sleep(3 * 60 * 60 + trnd)
            except Exception as e:
                await asyncio.sleep(30)
                continue
          else:
              break
      else:
          with open('users.json', 'r') as f:
              data = json.load(f)
              data[user_id]['auto_elon'] = False
          with open('users.json', 'w') as f:
              json.dump(data, f, indent=2)