import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/hist/strikes?token={token}&ticker=SPY&tradeDate=2024-08-05&dte=40,50&delta=.15,.30&fields=ticker,tradeDate,expirDate,dte,strike,stockPrice,callBidPrice,callAskPrice,putBidPrice,putAskPrice,delta"

print("Requesting ORATS Strikes History for SPY on 2024-08-05 (the VIX spike day)...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
