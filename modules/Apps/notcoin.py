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

@Client.on_message(filters.command(["notcoin", "notc", "нотк", "ноткоин" ], prefixes=pref_p)& filters.me)
async def notcoin(client, message):
    try:
        user_id = str((await client.get_me()).id)
        session = requests.Session()
        web_view = await client.invoke(RequestWebView(
            peer=await client.resolve_peer('@notcoin_bot'),
            bot=await client.resolve_peer('@notcoin_bot'),
            platform='android',
            from_bot_menu=False,
            url='https://farm.joincommunity.xyz/'
        ))
        auth_url = web_view.url
        session.proxies = {
            "http": f"https://{GET_PROXY(user_id)}"
        }
        payload =  {"webAppData": unquote(auth_url).split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]}
        session.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-language": "en-US,en;q=0.9,fa;q=0.8",
            "Content-Type": "application/json",
            "Origin": "https://farm.joincommunity.xyz",
            "Priority": "u=0, i",
            "Referer": "https://farm.joincommunity.xyz/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', 
            "sec-ch-ua-mobile": "?1", 
            "sec-ch-ua-platform": '"Android"', 
            "Sec-Fetch-Dest": "empty", 
            "Sec-Fetch-Mode": "cors", 
            "Sec-Fetch-Site": "same-site", 
            "User-Agent": get_UA(user_id)
        }
        resp = session.post('https://clicker-api.joincommunity.xyz/auth/webapp-session', json=payload)
        token = json.loads(resp.text)['data']["accessToken"]
        session.headers["Authorization"] = f"Bearer {token}"
        resp = session.get('https://clicker-api.joincommunity.xyz/pool/available')
        pools = json.loads(resp.text)["data"]['pools']
        await message.edit_text(f"<emoji id=5467583879948803288>🎮</emoji> Игра - NotCoin\nПулов - {len(pools)}")
    except Exception as ex:
        print(ex)