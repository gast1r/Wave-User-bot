import random
import json
def GET_PROXY(user_id):
    with open('users.json', 'r') as f:
        data = json.load(f)

    if user_id not in data: # Check if user_id exists at all
        data[user_id] = {'proxy': proxy_gen()} # Add a new entry for the user
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)

    if 'proxy' not in data[user_id]: # Check if proxy exists for the user
        data[user_id]['proxy'] = proxy_gen() # Generate and add a proxy if not
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=2)

    proxy = data[user_id]['proxy']
    return proxy

def proxy_gen():
    with open("proxy.txt", 'r') as file:
        lines = file.readlines() 
        r_int = random.randint(0, len(lines) - 1)
    if 0 <= r_int < len(lines):
        proxy = lines[r_int].strip()
        return proxy
     
