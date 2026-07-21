import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/hist/summaries?token={token}&ticker=SPY&tradeDate=2024-08-05&fields=ticker,tradeDate,contango,skewing,slope,confidence"

print("Requesting ORATS Summaries History for SPY on 2024-08-05...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
