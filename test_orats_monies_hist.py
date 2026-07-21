import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/hist/monies/implied?token={token}&ticker=SPY&tradeDate=2024-08-05&fields=ticker,tradeDate,expirDate,stockPrice,vol50,vol30,vol70,confidence"

print("Requesting ORATS Monies History (Implied) for SPY on 2024-08-05...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
