import urllib.request
import json
import time

def load_symbols():
    with open('sp500_symbols.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def fetch_confidence_batch(symbols, token):
    results = {}
    for i in range(0, len(symbols), 10):
        batch = symbols[i:i+10]
        ticker_str = ','.join(batch)
        url = f'https://api.orats.io/datav2/summaries?token={token}&ticker={ticker_str}&fields=ticker,confidence'
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                for item in data['data']:
                    results[item['ticker']] = item['confidence']
        except Exception as e:
            print(f'Batch failed for {ticker_str}: {e}')
        time.sleep(0.2)
        if (i // 10) % 10 == 0:
            print(f'Processed {i+len(batch)} of {len(symbols)} symbols...')
    return results

if __name__ == "__main__":
    from secrets_loader import get_secret
    token = get_secret('orats-api-token')
    symbols = load_symbols()
    print(f'Scanning {len(symbols)} S&P 500 symbols for confidence...')
    results = fetch_confidence_batch(symbols, token)

    qualifying = [t for t, c in results.items() if c > 0.90]
    print()
    print(f'Total symbols scanned: {len(results)}')
    print(f'Symbols with confidence > 90%: {len(qualifying)}')

    with open('sp500_confidence_results.txt', 'w') as f:
        for t in sorted(qualifying, key=lambda x: results[x], reverse=True):
            f.write(f'{t}: {results[t]*100:.2f}%\n')
    print('Full qualifying list saved to sp500_confidence_results.txt')
