from pyrogram import Client, filters
import re
import asyncio
import json
from  datetime import datetime


@Client.on_message(filters.chat(['eduardinvest', 'tolg1']))
async def major_combo_claimer(client, message):
    if "⭐️Major КОМБО" in message.text:
        keys = re.findall(r'\d+', message.text) 
        if keys:
            combo = ''
            for i, key in enumerate(keys):
                combo += f"{key}"
                if i < len(keys) - 1:
                    combo += "-"
            with open("combo.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if 'major' not in data:
                    data['major']['old_code'] = data['major']['code']
                    data['major']['code'] = combo
                    data['major']['date'] = datetime.now().timestamp()
                    with open('combo.json', 'w', encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                elif data['major']['code'] != combo:
                    data['major']['old_code'] = data['major']['code']
                    data['major']['code'] = combo
                    data['major']['date'] = datetime.now().timestamp()
                    with open('combo.json', 'w', encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            print("Числа не найдены")
    elif "📹 YouTube"  in message.text:
        text = message.text
        episodes = extract_episodes(text)
        with open("combo.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            data['elon'] = episodes
        with open("combo.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif "🤑BLUM код для видео"  in message.text:
        text = message.text.split('🤑BLUM код для видео')[1].split('Работаем в команде!')[0]
        code = re.findall(r'\d+', text) 
        match = re.search(r"^(.*?) : (\d+)$", text)
        name = text.split(':')[0].replace('\n', '').strip()
        code = text.split(':')[1].replace('\n', '').strip()
        print(name, '-', code)
        with open("combo.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if name not in  data:
                data['blum'] = {name:code}
                print(data)


def extract_episodes(text):
  episodes = {}
  lines = text.split('\n')
  for line in lines:
    if line.startswith('Episode'):
      parts = line.split(' - ')
      if len(parts) == 2:
        episode_name = parts[0].strip()
        episode_code = parts[1].strip()
        episodes[episode_name] = episode_code
  return episodes