import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/strikes?token={token}&ticker=SPY&dte=40,50&delta=.15,.30&fields=ticker,tradeDate,expirDate,dte,strike,stockPrice,callBidPrice,callAskPrice,putBidPrice,putAskPrice,delta"

print("Requesting ORATS Strikes endpoint for SPY (DTE 40-50, delta .15-.30)...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
