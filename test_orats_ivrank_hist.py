import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/hist/ivrank?token={token}&ticker=SPY&tradeDate=2024-08-05"

print("Requesting ORATS IV Rank History for SPY on 2024-08-05...")
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print("Response body:", e.read().decode())
