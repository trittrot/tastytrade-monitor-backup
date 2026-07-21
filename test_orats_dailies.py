import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/hist/dailies?token={token}&ticker=SPY&tradeDate=2024-08-05"

print("Requesting ORATS Daily Price for SPY on 2024-08-05...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
