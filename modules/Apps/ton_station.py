from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio, json
from utils.agents import get_UA
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
from datetime import datetime 


@Client.on_message(filters.command(["tonstationn", "тонсташион"], prefixes=pref_p)& filters.me)
async def tonstation(client, message):
    try:
        user_data = await client.get_me()
        user_id = str(user_data.id)
        web_view = await client.invoke(RequestWebView(
                peer=await client.resolve_peer('@tonstationgames_bot'),
                bot=await client.resolve_peer('@tonstationgames_bot'), 
                platform='android',
                from_bot_menu=True,
                url='https://tonstation.app/app/'
            ))
        auth_url = web_view.url
        session = requests.Session()
        session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
        text = ''
        session.headers.update({
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "Cache-Control": "no-chache",
                "Content-Type": "application/json",
                "Origin": "https://tonstation.app",
                "Pragma": "no-chache",
                "Priority": "u=1, i",
                "Referer": "https://tonstation.app/app/",
                'Host': 'tonstation.app',
                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": '"Android"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": get_UA(user_id)
            })
        token = unquote(auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        payload = {"initData": token}
        resp = session.get(f'https://tonstation.app/userprofile/api/v1/users/{user_id}/by-telegram-id')
        address = json.loads(resp.text)['address']
        resp = session.post('https://tonstation.app/userprofile/api/v1/users/auth', json=payload)
        token = json.loads(resp.text)['accessToken']
        session.headers['Authorization'] = f"Bearer {token}"
        payload = {"userId": user_id}
        resp = session.post('https://tonstation.app/farming/api/v1/user-rates/login', json=payload)
        #session.get(f'https://tonstation.app/quests/api/v1/quests?userId={user_id}&size=50') #quest
        resp = session.get(f'https://tonstation.app/farming/api/v1/farming/{user_id}/running')
        info = json.loads(resp.text)['data'][0]
        amount = info['amount']
        timeEnd = info['timeEnd']
        timestamp = datetime.fromisoformat(timeEnd).timestamp()
        current_timestamp = datetime.now().timestamp()
        isClaimed = info['isClaimed']
        _id = info['_id']
        if timestamp <= current_timestamp and isClaimed == False:
            payload = {"userId": user_id,"taskId": _id}
            session.post('https://tonstation.app/farming/api/v1/farming/claim', json=payload)
            await asyncio.sleep(3)
            payload = {"userId": user_id,"taskId": "1"}
            resp = session.post('https://tonstation.app/farming/api/v1/farming/start', json=payload)
            info = json.loads(resp.text)['data'][0]
            timeEnd = info['timeEnd']
            text = f'<emoji id=5427009714745517609>✅</emoji> Собрал с майнинг +{amount} $SOON'
            print('claim')
        resp = session.get(f'https://tonstation.app/balance/api/v1/balance/{address}/by-address')
        info = json.loads(resp.text)['data']
        balance = info['balance'][0]['balance']
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - TON Station\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance} $SOON {text}")
    except Exception as e:
        print(e)


@Client.on_message(filters.command(["atons", "autotons", "атонс"], prefixes=pref_p)& filters.me)
async def elon_auto(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_station" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_station']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_station'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"❌ Автоматический сбор TON Station - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_elon'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"✅ Автоматический сбор TON Station - включен") 
            asyncio.create_task(auto_station(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_station'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"❌ Автоматический сбор TON Station - выключен")
    await asyncio.sleep(2)
    await msg.delete()


async def auto_station(client, user_id, user_name):
  while True:
      with open('users.json', 'r') as f:
          data = json.load(f)
      if user_id in data and "auto_station" in data[user_id]:
          with open('users.json', 'r') as f:
              data = json.load(f)
              auto = data[user_id]['auto_station']
          if auto:
            session = requests.Session() 
            try:
                web_view = await client.invoke(RequestWebView(
                peer=await client.resolve_peer('@tonstationgames_bot'),
                bot=await client.resolve_peer('@tonstationgames_bot'), 
                platform='android',
                from_bot_menu=True,
                url='https://tonstation.app/app/'
                ))
                auth_url = web_view.url
                session.proxies = {
                    "http": f"https://{GET_PROXY(user_id)}"
                }
                text = ''
                session.headers.update({
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br, zstd",
                        "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                        "Cache-Control": "no-chache",
                        "Content-Type": "application/json",
                        "Origin": "https://tonstation.app",
                        "Pragma": "no-chache",
                        "Priority": "u=1, i",
                        "Referer": "https://tonstation.app/app/",
                        'Host': 'tonstation.app',
                        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                        "sec-ch-ua-mobile": "?1",
                        "sec-ch-ua-platform": '"Android"',
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "cross-site",
                        "User-Agent": get_UA(user_id)
                    })
                token = unquote(auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                payload = {"initData": token}
                resp = session.get(f'https://tonstation.app/userprofile/api/v1/users/{user_id}/by-telegram-id')
                address = json.loads(resp.text)['address']
                resp = session.post('https://tonstation.app/userprofile/api/v1/users/auth', json=payload)
                token = json.loads(resp.text)['accessToken']
                session.headers['Authorization'] = f"Bearer {token}"
                payload = {"userId": user_id}
                resp = session.post('https://tonstation.app/farming/api/v1/user-rates/login', json=payload)
                #session.get(f'https://tonstation.app/quests/api/v1/quests?userId={user_id}&size=50') #quest
                resp = session.get(f'https://tonstation.app/farming/api/v1/farming/{user_id}/running')
                info = json.loads(resp.text)['data'][0]
                amount = info['amount']
                timeEnd = info['timeEnd']
                timestamp = datetime.fromisoformat(timeEnd).timestamp()
                current_timestamp = datetime.now().timestamp()
                isClaimed = info['isClaimed']
                _id = info['_id']
                if timestamp <= current_timestamp and isClaimed == False:
                    payload = {"userId": user_id,"taskId": _id}
                    session.post('https://tonstation.app/farming/api/v1/farming/claim', json=payload)
                    await asyncio.sleep(3)
                    payload = {"userId": user_id,"taskId": "1"}
                    resp = session.post('https://tonstation.app/farming/api/v1/farming/start', json=payload)
                    info = json.loads(resp.text)['data'][0]
                    timeEnd = info['timeEnd']
                    time_wait = datetime.fromisoformat(time_wait).timestamp()
                    text = f' | Собрал с майнинг +{amount} $SOON'    
                resp = session.get(f'https://tonstation.app/balance/api/v1/balance/{address}/by-address')
                info = json.loads(resp.text)['data']
                balance = info['balance'][0]['balance']
                logger(f"{user_name} - TON Station |  Баланс - {balance} $SOON{text}")
                await asyncio.sleep(timestamp - current_timestamp)
            except Exception as e:
                await asyncio.sleep(30)
                continue
          else:
              break
      else:
          with open('users.json', 'r') as f:
              data = json.load(f)
              data[user_id]['auto_station'] = False
          with open('users.json', 'w') as f:
              json.dump(data, f, indent=2)