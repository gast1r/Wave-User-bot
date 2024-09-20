from pyrogram import Client, filters
from config import pref_p
import re
from pyrogram.raw.functions.messages import RequestWebView
from urllib.parse import unquote
import requests
import asyncio
import time
import datetime
import json
import urllib.parse
from utils.agents import generate_random_user_agent
import re

@Client.on_message(filters.command(["balance", "appbal"], prefixes=pref_p)& filters.me)
async def ibalance(client, message):
     start = time.time()
     session = requests.Session()
     session.headers.update({"authority": "0xiceberg.com", "method": "GET", "path": "/webapp/", "scheme": "https", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br, zstd", "accept-language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7", "Cache-Controk": "max-age=0", "content-type": "application/json", "Priority": "u=0, i", "Reffer": "https://0xiceberg.com/webapp/", "User-Agent": generate_random_user_agent()})
     web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('IcebergAppBot'),
            bot=await client.resolve_peer('IcebergAppBot'), #https://0xiceberg.com/api/v1/web-app/farming/
            platform='android',
            from_bot_menu=True,
            url='https://0xiceberg.com/webapp/'
        ))
     auth_url = web_view.url
     token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
     session.headers['X-Telegram-Auth'] = token
     resp =  session.get("https://0xiceberg.com/api/v1/web-app/balance/?format=json")
     data_dict = json.loads(resp.text)
     balance_ice = data_dict.get('amount')
     session.headers.update({"accept": "/", "accept-language": "en-US,en;q=0.9,fa;q=0.8", "content-type": "application/json", "Priority": "u=1, i", "Reffer": "https://telegram.blum.codes/", "User-Agent": generate_random_user_agent()})
     web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('BlumCryptoBot'),
            bot=await client.resolve_peer('BlumCryptoBot'),
            platform='android',
            from_bot_menu=False,
            url='https://telegram.blum.codes/'
        ))
     auth_url = web_view.url
     s = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
     json_data = {"query": s}
     resp = session.post("https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data)
     resp = resp.json()
     session.headers['Authorization'] = "Bearer " + (resp).get("token").get("access")
     resp =  session.get("https://game-domain.blum.codes/api/v1/user/balance")
     resp_json = resp.json()
     ticket = resp_json['playPasses']
     balance_blum = resp_json['availableBalance']
     web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('pocketfi_bot'),
            bot=await client.resolve_peer('pocketfi_bot'), #
            platform='android',
            from_bot_menu=True,
            url='https://0xiceberg.com/webapp/'
        ))
     auth_url = web_view.url
     token = string=unquote(string=auth_url.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
     session.headers['Telegramrawdata'] = token
     resp = session.get("https://gm.pocketfi.org/mining/getUserMining")
     data_dict = json.loads(resp.text)
     user = data_dict.get('userMining')
     balance_switch = round(float(user.get('gotAmount')), 2)
     finish = time.time()
     res = finish - start
     ago_time = round(res, 3)
     await message.edit_text(f"<emoji id=5375296873982604963>💰</emoji> Баланс - {balance_ice} ice\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance_blum} blum's (Tickets - {ticket})\n<emoji id=5375296873982604963>💰</emoji> Баланс - {balance_switch} $SWITCH\n||Потребовалось {ago_time} сек||")