import aiohttp
import random
from colorama import Fore
import time
import json
import asyncio
from datetime import datetime
import time
import string

proxies = ['35.185.196.38:3128', '43.153.207.93:3128', '136.228.160.250:5678', '98.191.0.47:4145', '184.178.172.23:4145', '142.54.239.1:4145', '184.185.2.12:4145', '72.195.34.60:2739', '184.178.172.25:15291', '104.200.135.46:4145', '74.208.26.199:37182 ', '160.86.242.23:8080', '142.54.232.6:4145',  '70.166.167.38:57728', '139.162.78.109:1080', '68.71.254.6:4145', '91.223.52.141:5678', '184.181.217.213:4145', '98.188.47.132:4145', '192.111.137.34:18765', '128.199.202.122:1080', '174.64.199.79:4145',  '109.197.152.1:1080', '184.181.217.210:4145', '154.12.178.107:29985',
            '103.216.50.224:8080', '109.61.42.223:80', '208.65.90.21:4145', '159.223.34.114:3128', '128.199.136.56:3128', '13.83.94.137:3128', '122.155.165.191:3128', '198.49.68.80:80', '103.237.144.232:1311', '67.43.227.228:10005', '62.33.53.248:3128', '43.134.121.40:3128', '43.133.59.220:3128', '181.188.27.162:8080', '200.174.198.86:8888', '157.230.188.193:3128', '166.1.22.160:8080', '34.97.45.196:8561', '152.42.224.138:3128', '35.185.196.38:3128', '47.90.205.231:33333', '39.112.180.187:8080', '187.141.125.210:8080', '212.110.188.204:34411', '212.110.188.204:34411', '43.134.68.153:3128',  '3.123.150.192:3128',  '13.38.176.104:3128', '13.56.192.187:3128', '8.219.97.248:80', '46.51.249.135:3128', '99.80.11.54:3128', '47.74.40.128:7788', '44.195.247.145:80', '47.251.70.179:80', '79.175.189.51:1080', '64.23.176.37:3128', '172.104.39.91:80', '45.240.182.197:1981', '160.86.242.23:8080', '154.236.177.100:1977', '5.189.184.6:80', '24.199.84.240:3128', '47.88.31.196:8080', '152.32.67.243:10101', '43.134.32.184:3128', '149.28.134.107:2020', '114.129.2.82:8081', '8.220.205.172:8080', '189.240.60.171:9090', '181.198.53.6:3128', '85.172.107.9:8952', '171.231.28.200:49236', '164.163.42.30:10000', '119.96.188.171:30000', '189.240.60.164:9090', '103.217.216.12:1111', '61.129.2.212:8080', '177.44.161.8:3128']
i = 0
r = random.randint(0,len(proxies) - 1)
proxy = f"http://{proxies[r]}"
print(f"Проксей - {len(proxies) - 1}")
async def gen_key(apptoken, game, promo):
    global i
    global proxy
    while True:
        id_1 = random.randint(1000000000000, 9999999999999)
        id_2 = random.randint(1000000000000000000, 9999999999999999999)
        try:
            async with aiohttp.ClientSession() as session:
                start = time.time()
                resp = await session.post("https://api.gamepromo.io/promo/login-client",
                                        headers={}, 
                                        json={"appToken": apptoken,
                                              "clientId": f"{id_1}-{id_2}",
                                              "clientOrigin": "deviceid"}, proxy=proxy)
                if resp.status != 200:
                    response_text = await resp.text()
                    if "TooManyIpRequest" in response_text:
                        await asyncio.sleep(2)
                        r = random.randint(0, len(proxies) - 1)
                        proxy = f"http://{proxies[r]}"
                    await asyncio.sleep(5)
                    continue
                    
                info = await resp.json() 
                auth = info.get("clientToken")
                if not auth:
                    await asyncio.sleep(5)
                    continue
                while True:
                        event_id = generate_random_string()
                        async with session.post("https://api.gamepromo.io/promo/register-event",
                                                headers={'Authorization': f"Bearer {auth}", 'Host': 'api.gamepromo.io', 'Content-Type': 'application/json'},
                                                json={"promoId": promo,
                                                      "eventId": f"{event_id}",
                                                      "eventOrigin":"undefined"}) as resp:
                            if resp.status != 200:
                                response_text = await resp.text()
                                await asyncio.sleep(20)
                                continue
                            
                            info = await resp.json()
                            status = info.get("hasCode")
                            if status:
                                async with session.post("https://api.gamepromo.io/promo/create-code",
                                                        headers={"Authorization": f"Bearer {auth}"},
                                                        json={"promoId": promo}) as resp:
                                    code_info = await resp.json()
                                    code = code_info.get("promoCode")
                                    if code:
                                        finish = time.time()
                                        res = round(finish - start)
                                        i += 1
                                        with open(f"promo_key/{game}_keys.txt", "a", encoding="utf-8") as text_file:
                                            text_file.write(f"{code}\n")
                                        with open(f"promo_key/{game}_keys.txt", "r", encoding="utf-8") as text_file:
                                            lines = text_file.readlines()
                                        now_date = datetime.today().strftime('%H:%M:%S')
                                        print(Fore.GREEN + f"{now_date} | Total promo codes {len(lines)} ({game}).Added ({i}) Spend {res} sec")
                                    break

        except Exception as e:
            r = random.randint(0, len(proxies) - 1)
            proxy = f"http://{proxies[r]}"
            await asyncio.sleep(10)


def generate_random_string():
    lengths = [8, 4, 4, 4, 12]
    parts = []
    for length in lengths:
        part = ''.join(random.choices(string.hexdigits.lower(), k=length))
        parts.append(part)
    return '-'.join(parts)

async def main():
    with open(f"cfg.txt", "r", encoding="utf-8") as text_file:
        lines = text_file.readlines()
        game = int(lines[1 - 1].strip())
    if game == 1:
        temp = "train"
        apptoken = "82647f43-3f87-402d-88dd-09a90025313f"
        promo = "c4480ac7-e178-4973-8061-9ed5b2e17954"
    elif game == 2:
        temp = "cube"
        apptoken = "d1690a07-3780-4068-810f-9b5bbf2931b2"
        promo = "b4170868-cef0-424f-8eb9-be0622e8e8e3"
    elif game == 3:
        temp = "merge"
        apptoken = "8d1cc2ad-e097-4b86-90ef-7a27e19fb833"
        promo = "dc128d28-c45b-411c-98ff-ac7726fbaea4"
    elif game == 4:
        temp = "twerk"
        apptoken = "61308365-9d16-4040-8bb0-2f4a4c69074c"
        promo = "61308365-9d16-4040-8bb0-2f4a4c69074c"
    elif game == 5:
        temp = "polysphere"
        apptoken = "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71"
        promo = "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71"
    elif game == 6:
        temp = "zoo"
        apptoken = "b2436c89-e0aa-4aed-8046-9b0515e1c46b"
        promo = "b2436c89-e0aa-4aed-8046-9b0515e1c46b"
    elif game == 7:
        temp = "trim"
        apptoken = "ef319a80-949a-492e-8ee0-424fb5fc20a6"
        promo = "ef319a80-949a-492e-8ee0-424fb5fc20a6"
    elif game == 8:
        temp = "fluff"
        apptoken = "112887b0-a8af-4eb2-ac63-d82df78283d9"
        promo = "112887b0-a8af-4eb2-ac63-d82df78283d9"
    elif game == 9:
        temp = "tile"
        apptoken = "e68b39d2-4880-4a31-b3aa-0393e7df10c7"
        promo = "e68b39d2-4880-4a31-b3aa-0393e7df10c7"
    elif game == 10:
        temp = "stone"
        apptoken = "04ebd6de-69b7-43d1-9c4b-04a6ca3305af"
        promo = "04ebd6de-69b7-43d1-9c4b-04a6ca3305af"
    elif game == 11:
        temp = "bounce"
        apptoken = "bc72d3b9-8e91-4884-9c33-f72482f0db37"
        promo = "bc72d3b9-8e91-4884-9c33-f72482f0db37"
    elif game == 12:
        temp = "ball"
        apptoken = "4bf4966c-4d22-439b-8ff2-dc5ebca1a600"
        promo = "4bf4966c-4d22-439b-8ff2-dc5ebca1a600"
    elif game == 13:
        temp = "pin"
        apptoken = "d2378baf-d617-417a-9d99-d685824335f0"
        promo = "d2378baf-d617-417a-9d99-d685824335f0"
    elif game == 14:
        temp = "count"
        apptoken = "4bdc17da-2601-449b-948e-f8c7bd376553"
        promo = "4bdc17da-2601-449b-948e-f8c7bd376553"
    elif game == 15:
        temp = "infected"
        apptoken = "eb518c4b-e448-4065-9d33-06f3039f0fcb"
        promo = "eb518c4b-e448-4065-9d33-06f3039f0fcb"
    elif game == 16:
        temp = "among"
        apptoken = "daab8f83-8ea2-4ad0-8dd5-d33363129640"
        promo = "daab8f83-8ea2-4ad0-8dd5-d33363129640"
    elif game == 17:
        temp = "factory"
        apptoken = "d02fc404-8985-4305-87d8-32bd4e66bb16"
        promo = "d02fc404-8985-4305-87d8-32bd4e66bb16"
    num_calls = 50
    print("Game - ", temp)
    tasks = [gen_key(apptoken, temp, promo) for _ in range(num_calls)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
