import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/monies/implied?token={token}&ticker=SPY&fields=ticker,tradeDate,expirDate,stockPrice,vol50,vol30,vol70,confidence"

print("Requesting ORATS Monies (Implied) for SPY...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
