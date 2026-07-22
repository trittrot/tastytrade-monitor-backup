import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
symbols = ['DIA','EEM','EWW','EWZ','FXI','GDX','GDXJ','GLD','IWM','QQQ','SLV','SMH','SPY','TLT','TQQQ','USO','UVXY','VXX','XLE','XLU','XOP']

results = []
for i in range(0, len(symbols), 10):
    batch = symbols[i:i+10]
    ticker_str = ','.join(batch)
    url = f"https://api.orats.io/datav2/summaries?token={token}&ticker={ticker_str}&fields=ticker,confidence"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
        for item in data['data']:
            results.append((item['ticker'], item['confidence']))

results.sort(key=lambda x: x[1], reverse=True)

print("Symbol   Confidence")
print("-" * 25)
for ticker, conf in results:
    flag = " PASS" if conf > 0.90 else ""
    print(f"{ticker:6s}   {conf:.4f}{flag}")

passed = [r for r in results if r[1] > 0.90]
print()
print(f"Symbols with confidence > 90%: {len(passed)} of {len(results)}")
