import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
ticker = "SPY"
fields = "ticker,tradeDate,ivHvXernRatio,orHvXern20d,slopeFcst"
url = f"https://api.orats.io/datav2/cores?token={token}&ticker={ticker}&fields={fields}"

print("Testing on Core General endpoint...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
