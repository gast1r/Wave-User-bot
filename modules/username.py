from pyrogram import Client, filters
from pyrogram.errors import UsernamePurchaseAvailable
from config import pref_p
import requests
from bs4 import BeautifulSoup


@Client.on_message(filters.command(["username", "tag", "тег"], prefixes=pref_p) & filters.me)
async def user_name(client, message): 
    user_name = message.command[1].replace('@', '')
    try:
        avaibale = await client.check_username("me", user_name)
    except UsernamePurchaseAvailable:
        resp = requests.post(f'https://fragment.com/username/{user_name}')
        soup = BeautifulSoup(resp.content, 'html.parser')
        cost_ton = soup.find('div', class_='table-cell-value tm-value icon-before icon-ton').text
        cost_USDT = soup.find('div', class_='table-cell-desc').text
        table = soup.find('time', class_='tm-countdown-timer')
        data_vals = []
        for tag in table.find_all(True, {'data-val': True}):
            data_vals.append(tag['data-val'])
        time_end = f"{data_vals[0]} {str(data_vals[1]) + str(data_vals[2])} час(ов) {str(data_vals[3]) + str(data_vals[4])} минут(ы) {str(data_vals[5]) + str(data_vals[6])} секунд(ы)"
        url = "https://v6.exchangerate-api.com/v6/5556ecb03068df0dd514fae9/latest/USD"
        response = requests.get(url, headers={"UserAgent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"})
        data = response.json()
        if 'conversion_rates' in data:
            rate = int(data['conversion_rates']['RUB'])
        number = float(cost_USDT.replace("~", "").replace(" ", "").replace("$", "").replace(",", ""))
        cost_RUB = format_number(number* rate)
        number = format_number(number)
        await message.edit_text(f"<emoji id=5411558372329667998>🌐</emoji> Юзернейм @{user_name} доступен для покупки на [Fragment.com](https://fragment.com/username/{user_name})\n<blockquote> Краткая информация:\nЦена - {cost_ton} TON ({number} USDT/{cost_RUB} RUB)\n До окончание осталось - {time_end}</blockquote>")
        return
    if avaibale == False:
        resp = requests.post(f'https://fragment.com/username/{user_name}')
        soup = BeautifulSoup(resp.content, 'html.parser')
        table = soup.find('span', class_='tm-section-header-status tm-status-taken').text
        if table == "Taken":
           await message.edit_text(f"<emoji id=5465665476971471368>❌</emoji> Юзернейм @{user_name} занят информация на [Fragment](https://fragment.com/username/{user_name}).\n<blockquote><emoji id=5472146462362048818>💡</emoji> Вы можете предложить цену и владелиц тега может продать его вам.</blockquote>")
        else:
            pass
    else:
        await message.edit_text(f"<emoji id=5427009714745517609>✅</emoji> Юзернейм @{user_name} свободен")
        
def format_number(number):
  formatted_number = f"{number:,.3f}"
  # Удаляем нули в конце, если они есть
  if formatted_number.endswith(".000"):
    formatted_number = formatted_number[:-4]
  return formatted_number