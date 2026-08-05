import urllib.request
import json
import time
import asyncio
from secrets_loader import get_secret
from alerts import send_alert
from tastytrade.watchlists import PrivateWatchlist
from auth import authenticate_production

THRESHOLD = 0.005

def load_symbols():
    with open('sp500_symbols.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def fetch_mwadj30_batch(symbols, token):
    results = {}
    for i in range(0, len(symbols), 10):
        batch = symbols[i:i+10]
        ticker_str = ','.join(batch)
        url = f'https://api.orats.io/datav2/summaries?token={token}&ticker={ticker_str}&fields=ticker,mwAdj30'
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                for item in data['data']:
                    val = item.get('mwAdj30')
                    if val is not None:
                        results[item['ticker']] = val
        except Exception as e:
            print(f'Batch failed for {ticker_str}: {e}')
        time.sleep(0.2)
    return results

async def update_tastytrade_watchlist(symbols):
    session = authenticate_production()
    watchlist = await PrivateWatchlist.a_get(session, 'Orats SPY mwAdj30')
    watchlist.watchlist_entries = []
    for s in symbols:
        watchlist.add_symbol(s, 'Equity')
    await watchlist.a_update(session)

def run_scan():
    try:
        token = get_secret('orats-api-token')
        symbols = load_symbols()
        print('Scanning ' + str(len(symbols)) + ' S&P 500 symbols for mwAdj30...')
        results = fetch_mwadj30_batch(symbols, token)

        qualifying = sorted([t for t, v in results.items() if v < THRESHOLD], key=lambda x: results[x])
        print('Total scanned: ' + str(len(results)) + '  Qualifying (mwAdj30 < ' + str(THRESHOLD) + '): ' + str(len(qualifying)))

        try:
            asyncio.run(update_tastytrade_watchlist(qualifying))
            print('Tastytrade Orats SPY mwAdj30 watchlist updated with ' + str(len(qualifying)) + ' symbols')
        except Exception as e:
            print('Watchlist update failed (non-fatal): ' + str(e))

        sms_msg = 'Tastytrade: mwAdj30 scan complete - ' + str(len(qualifying)) + ' of ' + str(len(results)) + ' symbols qualify (below ' + str(THRESHOLD) + '). Watchlist updated.'
        send_alert(sms_msg)

    except Exception as e:
        send_alert('Tastytrade monitor: mwAdj30 scan FAILED - ' + str(e))
        raise

if __name__ == '__main__':
    run_scan()
