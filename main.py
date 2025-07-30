import requests
import json
import os
from datetime import datetime

ADDRESS = "TRYtrEkTFiZbuuzt7o7ac7TVeEC5PLsnQa"
TELEGRAM_TOKEN = "8149165281:AAEPR3WYg6rjAAFf9tdizK_cLRnukbAnsMw"
CHAT_ID = "374907547"
LAST_TX_FILE = "last_tx.txt"

def get_transactions(address):
    url = f"https://apilist.tronscanapi.com/api/transaction?address={address}&limit=1&sort=-timestamp"
    res = requests.get(url)
    data = res.json()
    return data.get("data", [])

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

def load_last_tx():
    if os.path.exists(LAST_TX_FILE):
        with open(LAST_TX_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_tx(tx_hash):
    with open(LAST_TX_FILE, "w") as f:
        f.write(tx_hash)

def main():
    txs = get_transactions(ADDRESS)
    if not txs:
        return

    last_known = load_last_tx()
    latest = txs[0]
    latest_hash = latest["hash"]

    if latest_hash == last_known:
        return  # nessuna nuova transazione

    # ✅ Formattazione dati
    tx_type = latest.get("contractTypeDesc", "Transfer")
    token_info = latest.get("tokenInfo", {})
    symbol = token_info.get("tokenAbbr", "TRX")
    amount = token_info.get("tokenDecimal", 6)

    # ✅ Calcolo valore leggibile
    value = latest.get("amount", 0)
    if value and int(value) > 0:
        try:
            value = int(value) / (10 ** int(token_info.get("tokenDecimal", 6)))
        except:
            value = value
    else:
        value = "?"

    sender = latest.get("ownerAddress", "N/A")
    timestamp = datetime.fromtimestamp(int(latest["timestamp"]) / 1000).strftime("%Y-%m-%d %H:%M:%S")

    msg = f"""📥 Nuova transazione {symbol} rilevata:
👤 Mittente: `{sender}`
💰 Importo: {value} {symbol}
📝 Tipo: {tx_type}
🕒 Ora: {timestamp}
🔗 Hash: {latest_hash[:10]}..."""

    send_telegram_message(msg)
    save_last_tx(latest_hash)

if __name__ == "__main__":
    main()
