import requests
import time
import threading

lay_egg_url = 'https://api.quackquack.games/nest/lay-egg'

def read_tokens_nest_ids(filename):
    tokens_nest_ids = []
    with open(filename, 'r') as file:
        for line in file:
            tokens_nest_ids.append(line.strip().split('|'))
    return tokens_nest_ids

def lay_egg_if_ready(token, nest_id, duck_id):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'nest_id': nest_id, 'duck_id': duck_id}
    response = requests.post(lay_egg_url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Lay egg successfully for nest_id: {nest_id} and duck_id: {duck_id}")
    else:
        print(f"Error laying egg for nest_id: {nest_id} and duck_id: {duck_id}")

def check_and_lay_eggs(tokens_nest_ids):
    while True:
        threads = []
        for token_info in tokens_nest_ids:
            token, *_ = token_info
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get('https://api.quackquack.games/nest/list-reload', headers=headers)
            if response.status_code == 200:
                data = response.json()
                for nest in data['data']['nest']:
                    nest_id = nest['id']
                    if nest['egg_config_id'] is None:
                        for duck in data['data']['duck']:
                            duck_id = duck['id']
                            if duck['status'] == 1:
                                thread = threading.Thread(target=lay_egg_if_ready, args=(token, nest_id, duck_id))
                                threads.append(thread)
                                thread.start()
                    else:
                        print(f"Nest {nest_id} already has an egg.")
            else:
                print(f"Error getting nest IDs: {response.status_code}")
        for thread in threads:
            thread.join()
        #time.sleep(1)  # Chờ 5 giây trước khi kiểm tra lại

tokens_nest_ids = read_tokens_nest_ids('tokens.txt')
check_and_lay_eggs(tokens_nest_ids)
