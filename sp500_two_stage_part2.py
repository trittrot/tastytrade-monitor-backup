addition = "\ndef fetch_iv_pct_batch(symbols, token):\n    results = {}\n    for i in range(0, len(symbols), 10):\n        batch = symbols[i:i+10]\n        ticker_str = ','.join(batch)\n        url = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={ticker_str}&fields=ticker,ivPct1y'\n        try:\n            with urllib.request.urlopen(url) as response:\n                data = json.loads(response.read())\n                for item in data['data']:\n                    results[item['ticker']] = item.get('ivPct1y')\n        except Exception as e:\n            print(f'IV percentile batch failed for {ticker_str}: {e}')\n        time.sleep(0.2)\n    return results\n"
with open('sp500_two_stage_scan.py', 'a') as f:
    f.write(addition)
print("Chunk 2 written")
