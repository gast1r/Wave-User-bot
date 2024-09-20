from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
from utils.agents import get_UA
from utils.claimer_logs import logger
from utils.proxy import GET_PROXY
import random, json


@Client.on_message(filters.command(["cubes", "кубы"], prefixes=pref_p)& filters.me)
async def cubes(client, message):
    user_data = await client.get_me()
    user_id = str(user_data.id)
    web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('@cubesonthewater_bot'),
            bot=await client.resolve_peer('@cubesonthewater_bot'), 
            platform='android',
            from_bot_menu=True,
            url='https://www.thecubes.xyz/'
        ))
    auth_url = web_view.url
    token = unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
    session = requests.Session()
    session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
    session.headers.update({
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "Content-Type": "application/json",
                "Origin": "https://www.thecubes.xyz",
                "Priority": "u=1, i",
                "Referer": "https://www.thecubes.xyz/",
                'Host': 'server.questioncube.xyz',
                "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": '"Android"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": get_UA(user_id)
                })
    payload = {"initData":token,"newRefData": "null"}
    resp = session.post("https://server.questioncube.xyz/auth", json=payload)
    auth = json.loads(resp.text)
    token = auth['token']
    mined_count = auth['mined_count']
    energy = int(auth['energy'])
    boxes_amount = auth['boxes_amount']
    drops_amount = auth['drops_amount']
    ban = auth['banned_until_restore']
    if ban == True:
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **CUBES**\nВы забанены")
    await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **CUBES**\n<emoji id=5364325049312498976>💰</emoji> Баланс - {drops_amount}\n<emoji id=5364189233856662906>❓</emoji> ? - {boxes_amount}\n<emoji id=5364049003174447332>⛏</emoji> Добыть всего - {mined_count}\n<emoji id=5431449001532594346>⚡️</emoji> Энергии - {energy}/1000")
    last_message = None
    while True:
        if energy > 30:
            await asyncio.sleep(1)
            new_message = f"<emoji id=5467583879948803288>🎮</emoji> Игра - **CUBES**\n<emoji id=5364325049312498976>💰</emoji> Баланс - {drops_amount}\n<emoji id=5364189233856662906>❓</emoji> ? - {boxes_amount}\n<emoji id=5364049003174447332>⛏</emoji> Добыть всего - {mined_count}\n<emoji id=5431449001532594346>⚡️</emoji> Энергии - {energy}/1000\n<emoji id=5364049003174447332>⛏</emoji> Добываю блоки..."
            if new_message != last_message:
                await message.edit_text(new_message)
                last_message = new_message 
            payload = {"token": token}
            resp = session.post("https://server.questioncube.xyz/game/mined", json=payload)
            if resp.status_code == 200:
                t_s = random.randint(5, 7)
                await asyncio.sleep(t_s)
                auth = json.loads(resp.text)
                mined_count = auth['mined_count']
                energy = int(auth['energy'])
                boxes_amount = auth['boxes_amount']
                drops_amount = auth['drops_amount']
            else:
                await asyncio.sleep(5)
        else:
            await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - **CUBES**\n<emoji id=5364325049312498976>💰</emoji> Баланс - {drops_amount}\n<emoji id=5364189233856662906>❓</emoji> ? - {boxes_amount}\n<emoji id=5364049003174447332>⛏</emoji> Добыть всего - {mined_count}\n<emoji id=5431449001532594346>⚡️</emoji> Энергии - {energy}/1000\nЗакончилась энергия")
            break 
        
@Client.on_message(filters.command(["acubes", "акубы"], prefixes=pref_p)& filters.me)
async def automatic_cubes(client, message):
    with open('users.json', 'r') as f:
            data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_cubes" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_cubes']
        if auto:
            data[user_id]['auto_cubes'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор Cubes - выключен") 
        else:
            data[user_id]['auto_cubes'] = True
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор Cubes - включен") 
            asyncio.create_task(auto_cubes(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_cubes'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор Cubes - выключен")
    await asyncio.sleep(3)
    await msg.delete()


async def auto_cubes(client, user_id, user_name):
  while True:
      with open('users.json', 'r') as f:
          data = json.load(f)
      if user_id in data and "auto_cubes" in data[user_id]:
          with open('users.json', 'r') as f:
              data = json.load(f)
              auto = data[user_id]['auto_cubes']
          if auto:
            session = requests.Session() 
            try:
                web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('@cubesonthewater_bot'),
                        bot=await client.resolve_peer('@cubesonthewater_bot'), 
                        platform='android',
                        from_bot_menu=True,
                        url='https://www.thecubes.xyz/'
                    ))
                auth_url = web_view.url
                token = unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                session = requests.Session()
                session.proxies = {
                        "http": f"https://{GET_PROXY(user_id)}"
                    }
                session.headers.update({
                            "Accept": "*/*",
                            "Accept-Encoding": "gzip, deflate, br, zstd",
                            "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                            "Content-Type": "application/json",
                            "Origin": "https://www.thecubes.xyz",
                            "Priority": "u=1, i",
                            "Referer": "https://www.thecubes.xyz/",
                            'Host': 'server.questioncube.xyz',
                            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                            "sec-ch-ua-mobile": "?1",
                            "sec-ch-ua-platform": '"Android"',
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "cross-site",
                            "User-Agent": get_UA(user_id)
                            })
                payload = {"initData":token,"newRefData": "null"}
                resp = session.post("https://server.questioncube.xyz/auth", json=payload)
                auth = json.loads(resp.text)
                token = auth['token']
                mined_count = auth['mined_count']
                energy = int(auth['energy'])
                boxes_amount = auth['boxes_amount']
                drops_amount = auth['drops_amount']
                ban = auth['banned_until_restore']
                if ban == True:
                    return
                while True:
                    if energy > 30:
                        payload = {"token": token}
                        resp = session.post("https://server.questioncube.xyz/game/mined", json=payload)
                        if resp.status_code == 200:
                            t_s = random.randint(5, 7)
                            auth = json.loads(resp.text)
                            mined_count = auth['mined_count']
                            energy = int(auth['energy'])
                            boxes_amount = auth['boxes_amount']
                            drops_amount = auth['drops_amount']                            
                            await asyncio.sleep(t_s)
                        else:
                            await asyncio.sleep(5)
                    else:
                        logger(f"ID {user_id}({user_name}) CUBES DONE!Info: Баланс - {drops_amount}| ? - {boxes_amount}| Добыть всего - {mined_count}| Энергии - {energy}/1000")
                        break     
                print(f'Cubes - Done ({user_name})')
                await asyncio.sleep(16 * 60 + 50 + random.randint(20,100))
            except Exception as e:
                print(e)
                break
          else:
              break
      else:
          with open('users.json', 'r') as f:
              data = json.load(f)
              data[user_id]['auto_cubes'] = False
          with open('users.json', 'w') as f:
              json.dump(data, f, indent=2)