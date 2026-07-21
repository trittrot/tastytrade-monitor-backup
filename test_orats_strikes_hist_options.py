import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/hist/strikes/options?token={token}&ticker=SPY&expirDate=2024-09-13&strike=542.5"

print("Requesting ORATS Strikes History by Options for SPY 542.5 strike, Sep 13 2024 expiry...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
