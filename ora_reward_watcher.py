from algosdk.v2client import algod
from algosdk.util import microalgos_to_algos
import base64

algod_token = 'Insert Token Here'
algod_port = 'http://Insert IP:Port here'
algod_client = algod.AlgodClient(algod_token, algod_port)

ora_asset_id = 1284444444
ora_miner_app_id = 1284326447
pool_address = 'TRCEY5UZGTATGTF5K3U42IMDT467D4EHV7S5MYJBMLMYARYJOZFATORMUM'


#EVERY 5 BLOCKS ORA IS REWARDED
last_block = 0
last_miner_effort = 0

while True:
    previous_block = algod_client.status()['last-round']
    if previous_block != last_block:
        last_block = previous_block
        app_info = algod_client.application_info(ora_miner_app_id)['params']['global-state']
        x, y = [base64.b64decode(x['key']).decode() for x in app_info], [y['value']['uint'] for y in app_info]
        app_info_dict = dict(zip(x, y))
        current_miner_effort = app_info_dict['current_miner_effort']
        new_last_miner_effort = app_info_dict['last_miner_effort']
        if new_last_miner_effort != last_miner_effort and last_block % 5 == 0:
            pool_ora_balance = float((next((asset['amount'] for asset in algod_client.account_info(pool_address).get('assets', []) if asset['asset-id'] == ora_asset_id), None)) / 100_000_000)
            pool_algo_balance = float(microalgos_to_algos(algod_client.account_info(pool_address)['amount']))
            algo_per_ora = pool_algo_balance / pool_ora_balance
            print(f'Price: {str(algo_per_ora * 1.05)[:5]} Algo per 1.05 Ora Reward')
            print(f'Last Miner Fees Paid: {str(microalgos_to_algos(new_last_miner_effort))[:5]} Algo at block {last_block}')
            print(f'Profit: {str((algo_per_ora * 1.05) - (float(microalgos_to_algos(new_last_miner_effort))))[:5]} Algo\n')
            last_miner_effort = new_last_miner_effort  
