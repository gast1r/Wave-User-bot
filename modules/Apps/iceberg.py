from pyrogram import Client, filters
from config import pref_p
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import json
from utils.agents import get_UA
import datetime
import asyncio
from utils.claimer_logs import logger

@Client.on_message(filters.command(["iceberg", "ice"], prefixes=pref_p)& filters.me)
async def ice(client, message):
     try:
        user_id = str((await client.get_me()).id)
        session = requests.Session()
        session.headers.update({"authority": "0xiceberg.com", "method": "GET", "path": "/webapp/", "scheme": "https", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "Cache-Controk": "max-age=0", "content-type": "application/json", "Priority": "u=0, i", "Reffer": "https://0xiceberg.com/webapp/", "User-Agent": get_UA(user_id)})
        await client.read_chat_history('IcebergAppBot')
        web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('IcebergAppBot'),
            bot=await client.resolve_peer('IcebergAppBot'),
            platform='android',
            from_bot_menu=True,
            url='https://0xiceberg.com/webapp/'
        ))
        auth_url = web_view.url
        token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        session.headers['X-Telegram-Auth'] = token
        resp = session.get("https://0xiceberg.com/api/v1/web-app/balance/?format=json")
        data_dict = json.loads(resp.text)
        balance = data_dict.get('amount')
        resp = session.get("https://0xiceberg.com/api/v1/web-app/farming/?format=json")
        data_dict = json.loads(resp.text)
        time_s = data_dict.get('stop_time')
     except:
        await message.edit_text("**У вас нету бота @IcebergAppBot, запустить его**")
        return
     hours, minutes, seconds = time_until(time_s)
     if seconds == 0:
        resp = session.delete("https://0xiceberg.com/api/v1/web-app/farming/collect/?format=json")
        resp = session.post("https://0xiceberg.com/api/v1/web-app/farming/?format=json")
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - ICEBERG\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance}\n✅ Собрал 100 ICE")
     else:
        if hours == "0":
            time_claim = f"{minutes} минут и {seconds} секунд"
        elif hours == "0" and minutes == "0":
            time_claim = f"{seconds} секунд"
        else:
            time_claim = f"{hours} часов, {minutes} минут и {seconds} секунд"
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - ICEBERG\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance}\n<emoji id=5452069934089641166>❓</emoji> До клейма осталось - {time_claim}")
         


async def autoice(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
          data = json.load(f)
        if user_id in data and "auto_ice" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_ice']
            if auto:
                try:
                    session = requests.Session()
                    session.headers.update({"authority": "0xiceberg.com", "method": "GET", "path": "/webapp/", "scheme": "https", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br, zstd", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "Cache-Controk": "max-age=0", "content-type": "application/json", "Priority": "u=0, i", "Reffer": "https://0xiceberg.com/webapp/", "User-Agent": get_UA(user_id)})
                    await client.read_chat_history('IcebergAppBot')
                    web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('IcebergAppBot'),
                        bot=await client.resolve_peer('IcebergAppBot'),
                        platform='android',
                        from_bot_menu=True,
                        url='https://0xiceberg.com/webapp/'
                    ))
                    auth_url = web_view.url
                    token = unquote(auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                    session.headers['X-Telegram-Auth'] = token
                    resp = session.get("https://0xiceberg.com/api/v1/web-app/balance/?format=json")
                    data_dict = json.loads(resp.text)
                    balance = data_dict.get('amount')
                    await asyncio.sleep(2)
                    resp = session.get("https://0xiceberg.com/api/v1/web-app/farming/?format=json")
                    data_dict = json.loads(resp.text)
                    time_s = data_dict.get('stop_time')
                    datetime_object = datetime.datetime.strptime(time_s, "%Y-%m-%dT%H:%M:%S.%fZ")
                    timestamp = datetime_object.timestamp()
                    now = datetime.datetime.utcnow().timestamp()
                    if now > timestamp:
                        session.delete("https://0xiceberg.com/api/v1/web-app/farming/collect/?format=json")
                        session.post("https://0xiceberg.com/api/v1/web-app/farming/?format=json")
                        resp = session.get("https://0xiceberg.com/api/v1/web-app/farming/?format=json")
                        data_dict = json.loads(resp.text)
                        time_s = data_dict.get('stop_time')
                        datetime_object = datetime.datetime.strptime(time_s, "%Y-%m-%dT%H:%M:%S.%fZ")
                        timestamp = datetime_object.timestamp()
                        now = datetime.datetime.utcnow().timestamp()
                        delta = timestamp - now
                        logger(f"{user_name} Iceberg claimed. Info: Balance - {balance}")
                    else:
                        delta = timestamp - now
                    await asyncio.sleep(delta)
                except Exception as e:
                    print(e)
                    with open('users.json', 'r') as f:
                        data = json.load(f)
                        data[user_id]['auto_ice'] = False
                    with open('users.json', 'w') as f:
                        json.dump(data, f, indent=2)
                    break
            else:
              break
        else:
          with open('users.json', 'r') as f:
              data = json.load(f)
              data[user_id]['auto_ice'] = False
          with open('users.json', 'w') as f:
              json.dump(data, f, indent=2)



@Client.on_message(filters.command(["aice", "aiceberg"], prefixes=pref_p)& filters.me)
async def icebergauto(client, message):
    with open('users.json', 'r') as f:
            data = json.load(f)
    user_id = str((await client.get_me()).id)
    if user_id in data and "auto_ice" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_ice']
        if auto:
            data[user_id]['auto_ice'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор Iceberg - выключен") 
        else:
            data[user_id]['auto_ice'] = True
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор Iceberg - включен") 
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_ice'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор Iceberg - выключен")
    await asyncio.sleep(3)
    await msg.delete()


def time_until(target_time_str):
  target_time = datetime.datetime.fromisoformat(target_time_str[:-1])
  now = datetime.datetime.utcnow()

  if now > target_time:
    return 0, 0, 0

  delta = target_time - now
  print(delta)
  hours, remainder = divmod(delta.seconds, 3600)
  minutes, seconds = divmod(remainder, 60)

  return hours, minutes, seconds
