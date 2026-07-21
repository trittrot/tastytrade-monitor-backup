import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
ticker = "SPY"
fields = "ticker,tradeDate,iv30d_orHvXern20d,rSlp30,slopeFcst,ivHvXernRatio,iv30d,orHvXern20d"
url = f"https://api.orats.io/datav2/summaries?token={token}&ticker={ticker}&fields={fields}"

print("Testing field names for SPY...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
