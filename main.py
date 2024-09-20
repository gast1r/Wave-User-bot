import asyncio
import os
from colorama import Fore
from pyrogram import Client, errors, enums
import json
from modules.Apps.tabi import auto_tabi
from modules.Apps.zavod import auto_zavod
from modules.Apps.blum import auto_blum
from modules.Apps.elon import auto_elon
from modules.Apps.pocketfi import auto_pock
from modules.Apps.hamster import automatic_hamster
from modules.Apps.win import auto_win_token
from modules.Apps.cubes import auto_cubes
from modules.Apps.okx_racer import auto_okx
from modules.Apps.major import auto_major
from modules.Apps.ton_station import auto_station
from modules.Apps.iceberg import autoice
from modules.Apps.race import auto_race
from modules.Apps.vertus import auto_vertus
from modules.Apps.seed import auto_seed
from modules.Apps.vertus import auto_vertus
from modules.Apps.timefarm import auto_timefarm
from modules.Apps.dogitators import auto_dogiators
from utils.agents import generate_random_user_agent
from multiprocessing import Process
from config import API_ID, API_HASH, SESSION_PATH, version


async def start_session(session_name):
    try:
        app = Client(session_name, API_ID, API_HASH,
                    plugins=dict(root='modules'), workdir=SESSION_PATH, app_version=f"WaveUserBot {version}", device_model='iPhone 16 Pro Max')
        await app.start()
        user = await app.get_me()
        user_id = str(user.id)
        user_name = str(user.username)
        await load_users_data(user_id)
        # asyncio.create_task(auto_tabi(app, user_id, user_name))
        # asyncio.create_task(auto_zavod(app, user_id, user_name))
        # asyncio.create_task(auto_blum(app, user_id, user_name))
        # # asyncio.create_task(auto_win_token(app, user_id, user_name))
        # asyncio.create_task(auto_elon(app, user_id, user_name))
        # asyncio.create_task(automatic_hamster(app, user_id, user_name))
        # asyncio.create_task(auto_pock(app, user_id, user_name))
        # asyncio.create_task(auto_cubes(app, user_id, user_name))
        # asyncio.create_task(auto_major(app, user_id, user_name))
        # asyncio.create_task(auto_station(app, user_id, user_name))
        # asyncio.create_task(autoice(app, user_id, user_name))
        # asyncio.create_task(auto_okx(app, user_id, user_name))
        # asyncio.create_task(auto_race(app, user_id, user_name))
        # asyncio.create_task(auto_seed(app, user_id, user_name))
        # asyncio.create_task(auto_vertus(app, user_id, user_name))
        # asyncio.create_task(auto_timefarm(app, user_id, user_name))
        # asyncio.create_task(auto_dogiators(app, user_id, user_name))
        print(Fore.GREEN + f"Userbot '{user_name}' started!")
        while True:
            await asyncio.sleep(5)
    except Exception as e:
        print(e)
        print(f"Ошибка в сессии '{session_name}'")
        return



async def load_users_data(user_id):
    async with asyncio.Lock():
        with open('users.json', 'r') as f:
            data = json.load(f)
            if user_id not in data:
                data[user_id] = {'point': [180, 250], 'spend': False, 'fastoff': False, 'blum_token': '', 'games': 0, 'spend_max': 0, 'game_st': False, 'pref': '.'}
                with open('users.json', 'w') as f:
                    json.dump(data, f, indent=2)
                    print("User added to db")
            else:
                pass

async def main():
    sessions = []
    for file in os.listdir(SESSION_PATH):
        if file.endswith(".session"):
            sessions.append(file.replace(".session", ""))

    print(Fore.BLUE + f"Найдено сессий: {len(sessions)}!")
    
    tasks = [start_session(session) for session in sessions]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())