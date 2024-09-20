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
import datetime
import json
from utils.agents import get_UA
from utils.claimer_logs import logger
import random
from utils.proxy import GET_PROXY


@Client.on_message(filters.command(["zavodd", "завод"], prefixes=pref_p)& filters.me)
async def Zavod(client, message):
    try:
        user_id = str((await client.get_me()).id)
        session = requests.Session()
        session.proxies = {
                    "http": f"https://{GET_PROXY(user_id)}"
                }
        session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd", 
            "Accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", 
            "Origin": "https://zavod.mdaowallet.com", 
            "Priority": "u=1, i", 
            "Referer": "https://zavod.mdaowallet.com/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
            "Sec-Ch-Ua-mobile": "?1",
            "Sec-Ch-Ua-platform": '"Android"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": get_UA(user_id)})
        web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('Mdaowalletbot'),
            bot=await client.resolve_peer('Mdaowalletbot'),
            platform='android',
            from_bot_menu=True,
            url='https://zavod-api.mdaowallet.com'
        ))
        auth_url = web_view.url
        token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        session.headers['Telegram-Init-Data'] = token
        resp = session.get("https://zavod-api.mdaowallet.com/user/farm")
        data = json.loads(resp.text)
        token = data.get('tokensPerHour')
        date_claim = data.get('lastClaim')
        if data.get('claimInterval') == None:
            await message.edit_text(f"Кажется вы еще не зарегистрировались в zavod @Mdaowalletbot")
            return
        date_inter = int(data.get('claimInterval')) / 1000 / 60 /60
        print(date_inter)
    except:
           print(Exception)
           await message.edit_text("**У вас нету бота @Mdaowalletbot, запустить его**")
           return
    resp = session.get("https://zavod-api.mdaowallet.com/user/profile")
    data = json.loads(resp.text)
    balance = round(data.get('tokens'),2)
    can_claim, text = check_time(date_claim, int(date_inter))
    if can_claim:
        resp = session.post("https://zavod-api.mdaowallet.com/user/claim")
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Zavod\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance} ZP\n<emoji id=5472030678633684592>💸</emoji> Получаешь {token} ZP в час\n✅ Заклеймил монетки")
    else:
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - Zavod\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance} ZP\n<emoji id=5472030678633684592>💸</emoji> Получаешь {token} ZP в час\n<emoji id=5452069934089641166>❓</emoji> До клейма осталось - {text}")

def check_time(time_str, add_hours):
  utc_datetime = datetime.datetime.fromisoformat(time_str[:-1])
  msk_datetime = utc_datetime + datetime.timedelta(hours=3)
  msk_datetime += datetime.timedelta(hours=add_hours)
  current_datetime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))
  if current_datetime.replace(tzinfo=None) >= msk_datetime.replace(tzinfo=None):  
    return True, 0
  else:
    curr = current_datetime.replace(tzinfo=None)
    difference = msk_datetime - curr 
    text = f"{difference.seconds // 3600} часов, "f"{difference.seconds // 60 % 60} минут, {difference.seconds % 60} секунд"
    return False, text
  


@Client.on_message(filters.command(["azavod", "autozavod", "азавод"], prefixes=pref_p)& filters.me)
async def automatic_zavod(client, message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_zavod" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_zavod']
        if auto:
            with open('users.json', 'w') as f:
                data[user_id]['auto_zavod'] = False
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор Zavod - выключен") 
        else:
            with open('users.json', 'w') as f:
                data[user_id]['auto_zavod'] = True
                json.dump(data, f, indent=2)
            msg = await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор Zavod - включен") 
            await auto_zavod(client, user_id, user_name)
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_zavod'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji>  Автоматический сбор Zavod - выключен")
    await asyncio.sleep(2)
    await msg.delete()

  
async def auto_zavod(client, user_id, user_name):
  while True:
      with open('users.json', 'r') as f:
          data = json.load(f)
      if user_id in data and "auto_zavod" in data[user_id]:
          with open('users.json', 'r') as f:
              data = json.load(f)
              auto = data[user_id]['auto_zavod']
          if auto:
            session = requests.Session()
            session.headers.update({"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br, zstd", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "Origin": "https://zavod.mdaowallet.com", "Priority": "u=1, i", "Referer": "https://zavod.mdaowallet.com/","sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "User-Agent": get_UA(user_id)})
            try:
                session.proxies = {
                    "http": f"https://{GET_PROXY(user_id)}"
                }
                web_view = await client.invoke(RequestWebView(
                  peer=await client.resolve_peer('Mdaowalletbot'),
                  bot=await client.resolve_peer('Mdaowalletbot'),
                  platform='android',
                  from_bot_menu=True,
                  url='https://zavod-api.mdaowallet.com'
                  ))
                auth_url = web_view.url
                token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
            except:
                await client.send_message("me", "**У вас нету бота @Mdaowalletbot, запустить его и автомизацию (.azavod)**")
                with open('users.json', 'r') as f:
                    data = json.load(f)
                    data[user_id]['auto_zavod'] = False
                with open('users.json', 'w') as f:
                    json.dump(data, f, indent=2)
                break
            session.headers['Telegram-Init-Data'] = token
            resp = session.get("https://zavod-api.mdaowallet.com/user/farm")
            if resp.status_code != 200:
                with open('users.json', 'r') as f:
                    data = json.load(f)
                    data[user_id]['auto_zavod'] = False
                with open('users.json', 'w') as f:
                    json.dump(data, f, indent=2)
                await client.send_message("me", "**У вас нету бота @Mdaowalletbot, запустить его и автомизацию (.azavod)**")
                break
            data = json.loads(resp.text)
            token = data.get('tokensPerHour')
            date_claim = data.get('lastClaim')
            
            date_inter = int(data.get('claimInterval')) / 1000 / 60 /60
            if date_inter == None:
                date_inter = 0
            resp = session.get("https://zavod-api.mdaowallet.com/user/profile")
            data = json.loads(resp.text)
            balance = round(data.get('tokens'),2)
            can_claim, text = check_time(date_claim, int(date_inter))
            if can_claim:
              resp = session.post("https://zavod-api.mdaowallet.com/user/claim")
              print(f'Zavod - Done ({user_name})')
              logger(f"ID {user_id}({user_name}) Zavod claimed. Info: Balance - {balance} Claim - {text}")
            trnd = random.randint(40, 100)
            await asyncio.sleep(date_inter * 60 * 60 + trnd)
          else:
              break
      else:
          with open('users.json', 'r') as f:
              data = json.load(f)
              data[user_id]['auto_zavod'] = False
          with open('users.json', 'w') as f:
              json.dump(data, f, indent=2)