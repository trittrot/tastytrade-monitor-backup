import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/strikes/options?token={token}&symbols=SPY"

print("Requesting ORATS Strikes by Options endpoint (underlying SPY spot check)...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
