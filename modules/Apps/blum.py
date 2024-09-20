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
from utils.agents import get_UA
import random
import requests
import asyncio
import json
import humanize
import datetime as dt
import subprocess
from utils.claimer_logs import logger
sessions = {}
@Client.on_message(filters.command(["blum","блум"], prefixes=pref_p) & filters.me)
async def blum(client, message):
     user_id = str((await client.get_me()).id)
     session = requests.Session()
     session.headers.update({"Accept": "application/json, text/plain, */*", "Accept-language": "en-US,en;q=0.9,fa;q=0.8", "Priority": "u=1, i", "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "Sec-Ch-Ua-Mobile": "?1", "Sec-Ch-Ua-Platform": "Android", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site",  "Accept-Encoding": "gzip, deflate, br, zstd", "content-type": "application/json", "Priority": "u=1, i", "Origin": "https://telegram.blum.codes", "User-Agent": get_UA(user_id)})
     with open('users.json', 'r') as f:
        data = json.load(f)
        POINTS = data[user_id]['point']
        Spend_T = data[user_id]['spend']
        fast_off = data[user_id]['fastoff']
        spend_max = data[user_id]['spend_max']
        #lang = data[user_id]['lang']
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
     resp = session.post("https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data)
     resp = resp.json()
     session.headers['Authorization'] = "Bearer " + (resp).get("token").get("access")
     with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['blum_session'] = session.headers['Authorization']
     with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
     session.headers['Authorization'] = data[user_id]['blum_session']
     resp = session.post("https://game-domain.blum.codes/api/v1/daily-reward?offset=-180")
     await asyncio.sleep(1)
     resp =  session.get("https://game-domain.blum.codes/api/v1/user/balance")
     resp_json = resp.json()
     ticket = resp_json['playPasses']
     bal = resp_json['availableBalance']
     timestamp = resp_json.get("timestamp")
     if resp_json.get("farming"):
            start_time = resp_json.get("farming").get("startTime")
            end_time = resp_json.get("farming").get("endTime")
     else:
         start_time = None
         end_time = None
     await message.edit_text(f"<emoji id=5350746136544037083>🤑</emoji> Игра - BLUM \n<emoji id=5418010521309815154>🎫</emoji> Билеты - {ticket} \n<emoji id=6264804606941859519>💰</emoji> Баланс - {bal}")
     await asyncio.sleep(2)
     if start_time is not None and end_time is not None and timestamp >= end_time:
         resp = session.post("https://game-domain.blum.codes/api/v1/farming/claim")
         resp_json = resp.json()
         bal = resp_json['availableBalance']
         await message.edit_text(f"<emoji id=5350746136544037083>🤑</emoji> Игра - BLUM \n<emoji id=5418010521309815154>🎫</emoji> Билеты - {ticket} \n<emoji id=6264804606941859519>💰</emoji> Баланс - {bal}\n<emoji id=5452069934089641166>❓</emoji> Logs: Забрал монетки")
         await asyncio.sleep(2)
         resp = session.post("https://game-domain.blum.codes/api/v1/farming/start")
     elif start_time is None and end_time is None:
        try:
            resp = session.post("https://game-domain.blum.codes/api/v1/farming/start")
            await message.edit_text(f"<emoji id=5350746136544037083>🤑</emoji> Игра - BLUM \n<emoji id=5418010521309815154>🎫</emoji> Билеты - {ticket} \n<emoji id=6264804606941859519>💰</emoji> Баланс - {bal}\n<emoji id=5452069934089641166>❓</emoji>Logs: <emoji id=5350746136544037083>🤑</emoji> Начал фарминг!")
            await asyncio.sleep(2)
        except:
            pass
     else:
         resp = session.get("https://game-domain.blum.codes/api/v1/user/balance")
         resp_json = resp.json()
         timestamp = resp_json.get("timestamp")
         start_time = resp_json.get("farming").get("startTime")
         end_time = resp_json.get("farming").get("endTime")
         timestamp = int(timestamp / 1000)
         end_time = int(end_time / 1000)
         delta = dt.timedelta(seconds=end_time-timestamp)
         _t = humanize.i18n.activate("ru_RU")
         o = humanize.precisedelta(delta)
         await message.edit_text(f"<emoji id=5350746136544037083>🤑</emoji> Игра - BLUM \n<emoji id=5418010521309815154>🎫</emoji> Билеты - {ticket} \n<emoji id=6264804606941859519>💰</emoji> Баланс - {bal}\n<emoji id=5452069934089641166>❓</emoji> Logs: До клейма монет осталось {o} !")
         await asyncio.sleep(2)
     game_started = data[user_id]['game_st']
     if game_started:
         await message.edit_text(f"<emoji id=5350746136544037083>🤑</emoji> Игра - BLUM \n<emoji id=5418010521309815154>🎫</emoji> Билеты - {ticket} \n<emoji id=6264804606941859519>💰</emoji> Баланс - {bal}  \n<emoji id=5452069934089641166>❓</emoji> Logs: Игра уже запущена")
         with open('global.json', 'r') as f:
             data = json.load(f)
             data['game_started'] = False
         with open('global.json', 'w') as f:
             json.dump(data, f)
         return
     if Spend_T:
         await asyncio.sleep(2)
         if ticket == 0:
                await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Недостаточно билетов. Ты имеешь {ticket} билетов")
                with open('global.json', 'r') as f:
                 data = json.load(f)
                 data['game_started'] = False
                with open('global.json', 'w') as f:
                     json.dump(data, f)
         elif ticket <= spend_max:
                await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Я не буду тратить билеты. Ты имеешь {ticket}")
                with open('global.json', 'r') as f:
                 data = json.load(f)
                 data['game_started'] = False
                with open('global.json', 'w') as f:
                 json.dump(data, f)
                 return
         else:
             await asyncio.sleep(3)
             await game_loop(message, user_id, ticket, spend_max, POINTS,session)
     else:
         await message.edit_text(f"<emoji id=5350746136544037083>🤑</emoji> Игра - BLUM \n<emoji id=5418010521309815154>🎫</emoji> Билеты - {ticket} \n<emoji id=6264804606941859519>💰</emoji> Баланс - {bal}  \n<emoji id=5452069934089641166>❓</emoji> Logs: <emoji id=5465665476971471368>❌</emoji> Я не буду тратить билеты. Ты имеешь {ticket}")
         return

async def game(message, games, POINTS, user_id, session):
    await asyncio.sleep(2)
    try:
        response = session.post('https://game-domain.blum.codes/api/v1/game/play')
    except Exception as e:
        await message.edit_text("ERR. {e}!")
    await message.edit_text(f"<emoji id=5350746136544037083>🤑</emoji> Игра {games} - Запустил 'DROP GAME'!")
    if 'message' in response.json():
            await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Ошибка. 'DROP GAME' не смогла запуститься")
            with open('users.json', 'r') as f:
                data = json.load(f)
                games = data[user_id]['games'] 
                data[user_id]['games'] = games - 1
                data[user_id]['game_st'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            with open('global.json', 'r') as f:
                data = json.load(f)
                games_g = data['games']
                data['games'] = games_g - 1
                data['game_started'] = False
            with open('global.json', 'w') as f:
                json.dump(data, f, indent=2)
            return
    text = (response.json())['gameId']
    await asyncio.sleep(30)
    count = random.randint(*POINTS)
    json_data = {
        'gameId': text,
        'points': count,
        }
    response = session.post('https://game-domain.blum.codes/api/v1/game/claim', json=json_data)
    await asyncio.sleep(3)
    resp =  session.get("https://game-domain.blum.codes/api/v1/user/balance")
    resp_json = resp.json()
    ticket = resp_json['playPasses']
    bal = resp_json['availableBalance']
    await message.edit_text(f"<emoji id=5350746136544037083>🤑</emoji> Игра {games}.\n<emoji id=5418010521309815154>🎫</emoji> Твои билеты: {ticket}\n<emoji id=6264804606941859519>💰</emoji> **Получил: {count}**\n<emoji id=6264804606941859519>💰</emoji> Баланс: **{bal}** blum's")
    with open('users.json', 'r') as f:
         data = json.load(f)
         games = data[user_id]['games'] 
         data[user_id]['game_st'] = False
    with open('users.json', 'w') as f:
         json.dump(data, f, indent=2)


@Client.on_message(filters.command(["settb", "settblum"], prefixes=pref_p)& filters.me)
async def settb(client, message):
    user_id = str((await client.get_me()).id)
    with open('users.json', 'r') as f:
        data = json.load(f)
        Spend_T = data[user_id]['spend']
        Points = data[user_id]['point']
        spend_m = data[user_id]['spend_max']
        Game_s = data[user_id]['game_st']
    if Spend_T:
        sp = "да"
    else:
        sp = "нет"
    start_point = Points[0]
    end_point = Points[1]
    point_st = f"{start_point}-{end_point}"
    await message.edit_text(f"**<emoji id=5350746136544037083>🤑</emoji> Настройки '.blum'**: \n<emoji id=6264804606941859519>💸</emoji> Блумов за 'Drop Game' - {point_st} \n<emoji id=5418010521309815154>🎫</emoji> Тратить билеты - {sp} \n<emoji id=5260702125708557233>✋</emoji> Остановить игру на {spend_m} билетe/ах")


@Client.on_message(filters.command(["fblum", "fixb"], prefixes=pref_p)& filters.me)
async def fixb(client, message):
    user_id = str((await client.get_me()).id)
    with open('users.json', 'r') as f:
        data = json.load(f)
        data[user_id]['game_st'] = False
    with open('users.json', 'w') as f:
        json.dump(data, f, indent=2)


@Client.on_message(filters.command(["spendb", "spblum"], prefixes=pref_p)& filters.me)
async def spend(client, message):
    user_id = str((await client.get_me()).id)
    with open('users.json', 'r') as f:
        data = json.load(f)
        Spend_T = data[user_id]['spend']
        if Spend_T:
            msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Трата билетов сейчас **отключена**.")
            data[user_id]['spend'] = False
        else:
            msg = await message.edit_text("<emoji id=5427009714745517609>✅</emoji> Трата билетов сейчас **включена**.")
            data[user_id]['spend'] = True
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)
    await asyncio.sleep(5)
    await msg.delete()


@Client.on_message(filters.command(["spendmb", "spmblum"], prefixes=pref_p)& filters.me)
async def spendmax(client, message):
    try:
        spend_max = int(message.command[1])
    except:
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Ошибка. Число не может быть меньше нуля.")
        await asyncio.sleep(3)
        await msg.delete()
        return
    if spend_max < 0:
        await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Ошибка. Число не может быть меньше нуля.")
    else:
        user_id = str((await client.get_me()).id)
        with open('users.json', 'r') as f:
            data = json.load(f)
            await message.edit_text(f"<emoji id=5260702125708557233>✋</emoji> Я остановлюсь тратить на {spend_max} билете/ах")
            data[user_id]['spend_max'] = spend_max
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)


@Client.on_message(filters.command(["gameblum", "gblum"], prefixes=pref_p)& filters.me)
async def gameblum(client, message):
    try:
        a = int(message.command[1])
        print(a)
        b = int(message.command[2])
    except:
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Ошибка. **Не найдены диапазоны**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    if a > b:
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Ошибка. **Минимум не может быть больше чем максимум.**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    elif b > 299:
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Ошибка. **Максимум может быть только не больше 299 блумов**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    elif a > 299:
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Ошибка. **Максимум может быть только не больше 299 блумов!**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    elif a  < 150:
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Ошибка. **Минимум не может быть меньше нуля**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    elif b  < 150:
        msg = await message.edit_text("<emoji id=5465665476971471368>❌</emoji> Ошибка. **Максимум не может быть меньше нуля**")
        await asyncio.sleep(3)
        await msg.delete()
        return
    else:
        user_id = str((await client.get_me()).id)
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['point'] = [a, b]
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)
        msg = await message.edit_text(f"<emoji id=6264804606941859519>💸</emoji> Теперь вы получаете с {a} до {b} Блумов за 1 игру")
        await asyncio.sleep(3)
        await msg.delete()


@Client.on_message(filters.command(["stopblum", "sblum"], prefixes=pref_p)& filters.me)
async def stopblum(client, message):
    user_id = str((await client.get_me()).id)
    msg = await message.edit_text("<emoji id=5427240268589968037>⛔️</emoji> Я прекращаю тратить билеты.")
    with open('users.json', 'r') as f:
        data = json.load(f)
        data[user_id]['fastoff'] = True
    with open('users.json', 'w') as f:
        json.dump(data, f, indent=2)
    await asyncio.sleep(3)
    await msg.delete()

@Client.on_message(filters.command(["infob", "iblum"], prefixes=pref_p)& filters.me)
async def infoblum(client, message):
    user_id = str((await client.get_me()).id)
    with open('global.json', 'r') as f:
        data = json.load(f)
        game_g = data['games']
        start = data['game_started']
    with open('users.json', 'r') as f:
        data = json.load(f)
        game_l = data[user_id]['games']
    if start:
        ge = "да"
    else:
        ge = "нет"
    total_blum = game_g * 240
    await message.edit_text(f"<emoji id=5350746136544037083>🎮</emoji> Информация о blum:\n <emoji id=6273617244178091939>🎮</emoji> Всего сыграли - {game_g} игр\n<emoji id=5260343246831237239>🎮</emoji> Ты сыграл - {game_l} игр(ы)\n<emoji id=5467583879948803288>🎮</emoji> Сейчас играют - {ge}\n<emoji id=5317005586431231027>🎮</emoji> Заработали юзеры - {total_blum} blum's")


async def game_loop(message,user_id, ticket, spend_max, POINTS, session):
    while True:
        with open('global.json', 'r') as f:
            global_data = json.load(f)
            games_g = global_data['games']
        with open('users.json', 'r') as f:
            data = json.load(f)
            games = data[user_id]['games']
            fast_off = data[user_id]['fastoff']
        resp = session.get("https://game-domain.blum.codes/api/v1/user/balance")
        resp_json = resp.json()
        ticket = resp_json['playPasses']
        if ticket <= 0:
            await asyncio.sleep(3)
            await message.edit_text("<emoji id=5260293700088511294>✋</emoji> Ошибка. Ты имеешь 0 Билетов.")
            with open('global.json', 'r') as f:
                data = json.load(f)
                data['game_started'] = False
            with open('global.json', 'w') as f:
                json.dump(data, f)
            break
        elif fast_off:
            await message.edit_text(f"<emoji id=5260293700088511294>✋</emoji> Я остановился играть в 'Drop Game'. Ты имеешь {ticket} билетов.")
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['fastoff'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            with open('global.json', 'r') as f:
                data_g = json.load(f)
                data_g['game_started'] = False
            with open('global.json', 'w') as f:
                json.dump(data_g, f)
            break
        elif ticket == spend_max:
            await message.edit_text("<emoji id=5260293700088511294>✋</emoji> Я достиг лимита. Я прекращаю играть в 'Drop Game'.")
            with open('global.json', 'r') as f:
                 data = json.load(f)
                 data['game_started'] = False
            with open('global.json', 'w') as f:
                 json.dump(data, f)
            break 
        elif not fast_off:
            try:
                resp = session.get("https://game-domain.blum.codes/api/v1/user/balance")
                resp_json = resp.json()
                ticket = resp_json['playPasses']
            except Exception as e:
                 await message.edit_text("Ошибка. {e}!")
                 return
            await asyncio.sleep(0.5)
            time_z = (ticket - spend_max) * 36
            tick = ticket - spend_max
            await message.edit_text(f"<emoji id=5361813743279821319>🤑</emoji> Я трачу твои билеты.<emoji id=5418010521309815154>🎫</emoji> Ты имееешь {ticket} Билетов.\n⌛️ Займет времени - {time_z} сек\n<emoji id=5418010521309815154>🎫</emoji> Потрачу {tick} билетов")
            games_g += 1
            games += 1
            with open('global.json', 'w') as f:
                global_data['games'] = games_g
                json.dump(global_data, f, indent=2)

            with open('users.json', 'w') as f:
                data[user_id]['games'] = games 
                data[user_id]['game_st'] = True
                json.dump(data, f, indent=2)

            await game(message, games, POINTS, user_id,session)
            await asyncio.sleep(5) 


@Client.on_message(filters.command(["ablum", "autoblum"], prefixes=pref_p)& filters.me)
async def blumauto(client, message):
    with open('users.json', 'r') as f:
            data = json.load(f)
    user = await client.get_me()
    user_id = str(user.id)
    user_name = str(user.first_name)
    if user_id in data and "auto_blum" in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            auto = data[user_id]['auto_blum']
        if auto:
            data[user_id]['auto_blum'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор Blum - выключен") 
        else:
            data[user_id]['auto_blum'] = True
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
            await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Автоматический сбор Blum - включен")
            asyncio.create_task(auto_blum(client, user_id, user_name))
    else:
        with open('users.json', 'r') as f:
            data = json.load(f)
            data[user_id]['auto_blum'] = False
        with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
        await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Автоматический сбор Blum - выключен")
    await asyncio.sleep(3)
    await message.delete()


async def auto_blum(client, user_id, user_name):
    while True:
        with open('users.json', 'r') as f:
            data = json.load(f)
        if user_id in data and "auto_blum" in data[user_id]:
            with open('users.json', 'r') as f:
                data = json.load(f)
                auto = data[user_id]['auto_blum']
            if auto:
                try:
                    session = requests.Session()
                    session.headers.update({"Accept": "application/json, text/plain, */*", "Accept-language": "en-US,en;q=0.9,fa;q=0.8", "Priority": "u=1, i", "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"', "Sec-Ch-Ua-Mobile": "?1", "Sec-Ch-Ua-Platform": "Android", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site",  "Accept-Encoding": "gzip, deflate, br, zstd", "content-type": "application/json", "Priority": "u=1, i", "Origin": "https://telegram.blum.codes", "User-Agent": get_UA(user_id)})
                    web_view = await client.invoke(RequestWebView(
                        peer=await client.resolve_peer('BlumCryptoBot'),
                        bot=await client.resolve_peer('BlumCryptoBot'),
                        platform='android',
                        from_bot_menu=False,
                        url='https://telegram.blum.codes/'
                    ))
                    auth_url = web_view.url
                    token = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
                    json_data = {"query": token}
                    try:
                        resp = session.post("https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP", json=json_data)
                        resp = resp.json()
                        ref_token = resp.get("token").get("refresh")
                        session.headers['Authorization'] = "Bearer " + (resp).get("token").get("access")
                        with open('users.json', 'r') as f:
                            data = json.load(f)
                            data[user_id]['blum_session'] = session.headers['Authorization']
                        with open('users.json', 'w') as f:
                            json.dump(data, f, indent=2)
                    except Exception as e:
                        break
                    session.post("https://game-domain.blum.codes/api/v1/daily-reward?offset=-180")
                    await asyncio.sleep(1)
                    resp =  session.get("https://game-domain.blum.codes/api/v1/user/balance")
                    resp_json = resp.json()
                    ticket = resp_json['playPasses']
                    balance = resp_json['availableBalance']
                    timestamp = resp_json.get("timestamp")
                    if resp_json.get("farming"):
                        start_time = resp_json.get("farming").get("startTime")
                        end_time = resp_json.get("farming").get("endTime")
                    else:
                        start_time = None
                        end_time = None
                        await asyncio.sleep(2)
                    if start_time is not None and end_time is not None and timestamp >= end_time:
                            resp = session.post("https://game-domain.blum.codes/api/v1/farming/claim")
                            resp_json = resp.json()
                            bal = resp_json['availableBalance']
                            await asyncio.sleep(2)
                            resp = session.post("https://game-domain.blum.codes/api/v1/farming/start")
                            text = "Claim and farm"
                    elif start_time is None and end_time is None:
                        try:
                            resp = session.post("https://game-domain.blum.codes/api/v1/farming/start")
                            await asyncio.sleep(2)
                            text = "farm"
                        except:
                            pass
                    else:
                        resp = session.get("https://game-domain.blum.codes/api/v1/user/balance")
                        resp_json = resp.json()
                        timestamp = resp_json.get("timestamp")
                        start_time = resp_json.get("farming").get("startTime")
                        end_time = resp_json.get("farming").get("endTime")
                        timestamp = int(timestamp / 1000)
                        end_time = int(end_time / 1000)
                        delta = dt.timedelta(seconds=end_time-timestamp)
                        _t = humanize.i18n.activate("ru_RU")
                        o = humanize.precisedelta(delta)
                        text = "wait"
                    trnd = random.randint(10, 120)
                    if text != "wait":
                        print(f'Blum - Done ({user_name})')
                        logger(f"ID {user_id}({user_name}) Blum claimed. Info: Balance - {balance} Ticket - {ticket} Text - {text}")
                    await asyncio.sleep(end_time - timestamp + trnd)
                except Exception as e:
                    print(e)
                    break
            else:
                break
        else:
            with open('users.json', 'r') as f:
                data = json.load(f)
                data[user_id]['auto_blum'] = False
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=2)
