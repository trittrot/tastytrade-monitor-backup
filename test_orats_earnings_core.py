import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
ticker = "AAPL"
fields = "ticker,tradeDate,absAvgErnMv,ernMvStdv,fcstErnEffct"
url = f"https://api.orats.io/datav2/cores?token={token}&ticker={ticker}&fields={fields}"

print("Requesting Core Earn absolute average earnings move for AAPL...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
