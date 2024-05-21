import requests
import threading
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Strategy để thử lại các yêu cầu
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

# Adapter HTTP với chiến lược thử lại
adapter = HTTPAdapter(max_retries=retry_strategy)

# Tạo session với thử lại và connection pooling
session = requests.Session()
session.mount("https://", adapter)

payload = {"type": 1}
url = 'https://api.quackquack.games/nest/collect'
url2 = 'https://api.quackquack.games/balance/get'
url3 = 'https://api.quackquack.games/golden-duck/reward'
url4 = 'https://api.quackquack.games/golden-duck/claim'
url_hatch = 'https://api.quackquack.games/nest/hatch'
collect_url = 'https://api.quackquack.games/nest/collect-duck'

def read_tokens_nest_ids(filename):
    tokens_nest_ids = []
    with open(filename, 'r') as file:
        for line in file:
            tokens_nest_ids.append(line.strip().split('|'))
    return tokens_nest_ids

def get_nest_ids(session, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = session.get('https://api.quackquack.games/nest/list-reload', headers=headers)
    if response.status_code == 200:
        data = response.json()
        nest_ids = [nest['id'] for nest in data.get('data', {}).get('nest', [])]
        for nest in data.get('data', {}).get('nest', []):
            egg_config_id = nest.get('egg_config_id')
            if egg_config_id is not None and egg_config_id >= 8:
                try:
                    response_hatch = session.post('https://api.quackquack.games/nest/hatch', json={'nest_id': nest['id']}, headers=headers)
                    response_hatch.raise_for_status()
                    print("Hatch successfully.")
                    time.sleep(1)
                except requests.RequestException:
                    pass
            try:
                collect_duck = session.post('https://api.quackquack.games/nest/collect-duck', json={'nest_id': nest['id']}, headers=headers)
                collect_duck.raise_for_status()
                print("collect successfully.")
            except requests.RequestException:
                pass
        return nest_ids
    else:
        return []

def process_nest(session, token_nest_id, idx):
    while True:
        token, *_ = token_nest_id
        nest_ids = get_nest_ids(session, token)
        if not nest_ids:
            return

        headers = {'Authorization': f'Bearer {token}'}
        for nest_id in nest_ids:
            data = {'nest_id': nest_id}
            try:
                response = session.post(url, json=data, headers=headers)
                response.raise_for_status()

                response = session.get(url3, headers=headers)
                if response.status_code == 200:
                    json_data = response.json()
                    amount = json_data["data"]["amount"]
                    data_type = json_data.get("data", {}).get("type")

                    if data_type == 0:
                        print('\033[91mTrúng cái nịt\033[0m')  # Red color
                    elif data_type == 1:
                        with open('tonclaim.txt', 'a') as file:
                            file.write(f'{idx}-ton-Amount: {amount}\n')
                        response = session.post(url4, json={"type": 2}, headers=headers)
                        print('\033[94m{}-ton-Amount: {}\033[0m'.format(idx, amount))  # Blue color
                    elif data_type == 2:
                        response = session.post(url4, json=payload, headers=headers)
                        print('\033[92m{}-Pepets-Amount: {}\033[0m'.format(idx, amount))  # Green color
                        with open('pepetsclaim.txt', 'a') as file:
                            file.write(f'{idx}-Pepets-Amount: {amount}\n')
                    elif data_type == 3:
                        response = session.post(url4, json=payload, headers=headers)
                        print('{}-Eggs-Amount: {}'.format(idx, amount))
                    else:
                        pass

                response = session.get(url2, headers=headers)
                response_json = response.json()
                account_data = response_json['data']['data']
                balance = account_data[2]['balance']
                print(f"{idx} | TỔNG SỐ TRỨNG VỊT 🐥: {balance}")

            except requests.RequestException:
                pass

def main():
    tokens_nest_ids = read_tokens_nest_ids('tokens.txt')
    threads = []
    for idx, token_nest_id in enumerate(tokens_nest_ids, start=1):
        thread = threading.Thread(target=process_nest, args=(requests.Session(), token_nest_id, idx))
        thread.start()
        threads.append(thread)
    
    # Chờ tất cả các luồng hoàn thành trước khi kết thúc chương trình
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
