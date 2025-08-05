# TRON Wallet Monitor (GitHub-Based)

✅ Monitora i wallet TRON e aggiorna i dati ogni 10 minuti via GitHub Actions.

## Wallet Monitorati
- `TRYtrEkTFiZbuuzt7o7ac7TVeEC5PLsnQa`
- `TDtibBQcXnjpYJszXGuFUEVMoceS6voKGZ`

## Funzionalità
- Estrazione transazioni via API Tronscan
- Salvataggio CSV automatico
- Notifiche Telegram
- Dashboard pubblica (GitHub Pages)

## Configurazione

1. Aggiungi i seguenti **segreti GitHub**:
   - `TELEGRAM_TOKEN`: token del tuo bot Telegram
   - `TELEGRAM_CHAT_ID`: ID del canale/chat

2. Abilita **GitHub Pages** puntando alla cartella `/dashboard`

3. Attiva **GitHub Actions** per il repo.

## Dashboard
Verrà pubblicata automaticamente su:

`https://<tuo-utente>.github.io/tron-wallet-monitor/`

