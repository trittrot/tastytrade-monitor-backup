import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
ticker = "SPY"
url = f"https://api.orats.io/datav2/cores?token={token}&ticker={ticker}&fields=tradeDate,contango,slope,slopepctile,mktWidthVol"

print(f"Requesting ORATS data for {ticker}...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
