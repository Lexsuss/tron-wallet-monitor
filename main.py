import requests
import pandas as pd
from datetime import datetime

WALLETS = [
    'TRYtrEkTFiZbuuzt7o7ac7TVeEC5PLsnQa',
    'TDtibBQcXnjpYJszXGuFUEVMoceS6voKGZ'
]

def get_transactions(address):
    url = f'https://apilist.tronscanapi.com/api/transaction?address={address}&limit=100&sort=-timestamp'
    response = requests.get(url)
    data = response.json()
    tx_list = data.get("data", [])
    return tx_list

def save_to_csv(address, transactions):
    simplified = []
    for tx in transactions:
        ts = tx.get('timestamp')
        amount = tx.get('contractData', {}).get('amount', 0)
        tx_type = tx.get('contractType')
        hash_ = tx.get('hash')
        sender = tx.get('ownerAddress')
        receiver = tx.get('toAddress')
        simplified.append({
            'timestamp': datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S') if ts else '',
            'amount': int(amount) / 1_000_000 if amount else 0,
            'type': tx_type,
            'hash': hash_,
            'from': sender,
            'to': receiver
        })
    df = pd.DataFrame(simplified)
    filename = f"data/wallet_{address[:6]}.csv"
    df.to_csv(filename, index=False)
    print(f"[✓] Salvato: {filename}")

if __name__ == "__main__":
    for wallet in WALLETS:
        print(f"🔍 Analizzo wallet: {wallet}")
        tx = get_transactions(wallet)
        save_to_csv(wallet, tx)
