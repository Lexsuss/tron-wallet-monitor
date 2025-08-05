import requests
import pandas as pd
from datetime import datetime
import os

# === CONFIG ===
WALLETS = [
    'TRYtrEkTFiZbuuzt7o7ac7TVeEC5PLsnQa',
    'TDtibBQcXnjpYJszXGuFUEVMoceS6voKGZ'
]
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("[!] Telegram non configurato.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_transactions(address):
    url = f'https://apilist.tronscanapi.com/api/transaction?address={address}&limit=20&sort=-timestamp'
    response = requests.get(url)
    data = response.json()
    return data.get("data", [])

def process_wallet(address):
    csv_path = f"data/wallet_{address[:6]}.csv"
    old_hashes = []
    if os.path.exists(csv_path):
        df_old = pd.read_csv(csv_path)
        old_hashes = df_old['hash'].tolist()
    transactions = get_transactions(address)
    new_rows = []
    for tx in transactions:
        tx_hash = tx.get("hash")
        if tx_hash in old_hashes:
            continue
        ts = tx.get("timestamp")
        amount = tx.get('contractData', {}).get('amount', 0)
        sender = tx.get('ownerAddress')
        receiver = tx.get('toAddress')
        date_str = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
        amount_fmt = int(amount) / 1_000_000 if amount else 0
        new_rows.append({
            "timestamp": date_str,
            "from": sender,
            "to": receiver,
            "amount": amount_fmt,
            "hash": tx_hash
        })
        # Notifica Telegram
        msg = f"📥 Nuova transazione rilevata!\n👤 Mittente: {sender[:8]}...\n💰 Importo: {amount_fmt} TRX\n📅 Ora: {date_str}\n🔗 Hash: {tx_hash[:12]}..."
        send_telegram_message(msg)

    if new_rows:
        df_new = pd.DataFrame(new_rows)
        if os.path.exists(csv_path):
            df_old = pd.read_csv(csv_path)
            df_full = pd.concat([df_new, df_old], ignore_index=True)
        else:
            df_full = df_new
        df_full.to_csv(csv_path, index=False)
        print(f"[✓] {len(new_rows)} nuove transazioni salvate in {csv_path}")
    else:
        print(f"[✓] Nessuna nuova transazione per {address[:8]}...")

if __name__ == "__main__":
    for wallet in WALLETS:
        process_wallet(wallet)
