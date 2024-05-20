import requests
import time
import concurrent.futures
while True:
    url = 'https://api.quackquack.games/nest/collect'
    url2 = 'https://api.quackquack.games/balance/get'
    url3 = 'https://api.quackquack.games/golden-duck/info'
    url4 = 'https://api.quackquack.games/golden-duck/collect'
    url_hatch = 'https://api.quackquack.games/nest/hatch'
    collect_url = 'https://api.quackquack.games/nest/collect-duck'

    def read_tokens_nest_ids(filename):
        tokens_nest_ids = []
        with open(filename, 'r') as file:
            for line in file:
                tokens_nest_ids.append(line.strip().split('|'))
        return tokens_nest_ids

    def get_nest_ids(token):
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('https://api.quackquack.games/nest/list-reload', headers=headers)
        if response.status_code == 200:
            data = response.json()
            nest_ids = [nest['id'] for nest in data.get('data', {}).get('nest', [])]
            for nest in data.get('data', {}).get('nest', []):
                egg_config_id = nest.get('egg_config_id')
                if egg_config_id is not None and egg_config_id >= 3:
                    try:
                        response_hatch = requests.post(url_hatch, json={'nest_id': nest['id']}, headers=headers)
                        response_hatch.raise_for_status()
                        print("Hatch successfully.")
                        time.sleep(1)
                        collect_duck = requests.post(collect_url, json={'nest_id': nest['id']}, headers=headers)
                        collect_duck.raise_for_status()
                        print("collect successfully.")
                    except requests.exceptions.RequestException as e:
                        pass
            return nest_ids
        else:
            pass
            return []

    def process_nest(token_nest_id, idx):
        while True:
            token, *_ = token_nest_id
            nest_ids = get_nest_ids(token)
            if not nest_ids:
                return
            
            headers = {'Authorization': f'Bearer {token}'}
            for nest_id in nest_ids:
                data = {'nest_id': nest_id}
                
                try:
                    response = requests.post(url, json=data, headers=headers)
                    response.raise_for_status()
                    
                    response = requests.post(url4, headers=headers)
                    response = requests.get(url3, headers=headers)
                    response = requests.get(url2, headers=headers)
                    response_json = response.json()
                    account_data = response_json['data']['data']
                    balance = account_data[2]['balance']
                    print(f"{idx} - Balance: {balance}")
                except requests.exceptions.RequestException as e:
                    pass

    if __name__ == "__main__":
        tokens_nest_ids = read_tokens_nest_ids('tokens.txt')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for idx, token_nest_id in enumerate(tokens_nest_ids, start=1):
                executor.submit(process_nest, token_nest_id, idx)
