import json
import random

def generate_random_user_agent():
 with open('UA.json', 'r') as file:
        ua_list = json.load(file)
 ua = random.choice(ua_list)
 return ua
def get_UA(user_id):
    user_id = str(user_id)
    with open('users.json', 'r') as f:
            data = json.load(f)
    if user_id not in data and "UA" not in data[user_id]:
        with open('users.json', 'r') as f:
            data = json.load(f)
            ua = data[user_id]['UA'] = generate_random_user_agent()
        with open('users.json', 'w') as f:
                    json.dump(data, f, indent=2)
        return ua
    else:
         with open('users.json', 'r') as f:
            data = json.load(f)
            ua = data[user_id]['UA']
         return ua
