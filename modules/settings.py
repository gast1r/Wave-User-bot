from pyrogram import Client, filters
from config import pref_p
import json

#This is not work(|Это не работает(
@Client.on_message(filters.command(["преф","preefe"], prefixes=".") & filters.me)
async def pref(client, message):
    await message.delete()
    pref_p = message.command[1]
    user_id = str((await client.get_me()).id)
    with open('users.json', 'r+', encoding="utf-8") as f:
         data = json.load(f)
         old = data[user_id]["pref_p"]
         pref_p = pref_p.replace(old, "г") 
         data[user_id]["pref"] = pref_p
    with open('users.json', 'w', encoding="utf-8") as f:
         json.dump(data, f, indent=2)
    await client.send_message(message.chat.id, f"<emoji id=5021905410089550576>✅</emoji>Ваш префикс был изменен на {pref_p}")

def yes_no(var):
     if var:
          return "<emoji id=5427009714745517609>✅</emoji>"
     else:
          return "<emoji id=5465665476971471368>❌</emoji>"
def checker(app, user_id, data):
     if user_id in data and app in data[user_id]:
          answer = yes_no(data[user_id][app])
          o_app, emoji = apps_orig(app)
          return f"{emoji}Авто-{o_app} - {answer}\n"
     else:
          return
def apps_orig(app):
     if app == "auto_tabi":
          return "Tabi", "🦁 "
     elif app == "auto_zavod":
          return "Zavod", "🏭 "
     elif app == "auto_ham":
          return "Hamster", "🐹 "
     elif app == "auto_okx":
          return "Okx", "<emoji id=5328290660246101415>📈</emoji> "
     elif app == "auto_blum":
          return "Blum", "<emoji id=5429503304038106656>💰</emoji> "
     elif app == "auto_ice":
          return "Iceberg", "🥶 "
     elif app == "auto_elon":
          return "X-Empire", "<emoji id=5231394776414178774>🎩</emoji> "
     elif app == "auto_pocket":
          return "Pocketfi", "<emoji id=5276424673834317384>🚀</emoji> "
     elif app == "auto_cubes":
          return "Cubes", "<emoji id=5363919733248773777>📦</emoji> "
     elif app == "auto_win":
          return "1Win", "<emoji id=5280697337365149723>📦</emoji> "
     elif app == "auto_major":
          return "Major", "<emoji id=5816707898696274976>⭐️</emoji> "
     elif app == "auto_racer":
          return "Race", "<emoji id=5328290660246101415>📈</emoji> "
     elif app == "auto_seed":
          return "Seed", "<emoji id=5449885771420934013>🌱</emoji> "
     elif app == "auto_vertus":
          return "Vertus", "<emoji id=5426931877053222753>🌐</emoji> "
     elif app == "auto_timefarm":
          return "Time Farm", "<emoji id=5451732530048802485>⏳</emoji> "
     elif app == "auto_dogiators":
          return "Dogiators", "<emoji id=5267237618529088267>👊</emoji> "
     elif app == "auto_station":
          return "Ton Station", "<emoji id=5258113810912267471>😉</emoji> "
     else:
          return "", ""
@Client.on_message(filters.command(["settapp","asett", "sapp"], prefixes=".") & filters.me)
async def settings(client, message):
     with open('users.json', 'r') as f:
          data = json.load(f)
     user_id = str((await client.get_me()).id)
     text = ""
     for app in data[user_id].keys():
        if app.startswith("auto_"):
             text += checker(app, user_id, data)
     await message.edit_text(f"<emoji id=5372981976804366741>🤖</emoji> Автомизация:\n{text}")