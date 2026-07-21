import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
ticker = "AAPL"
fields = "ticker,tradeDate,exErnIv30d,exErnIv90d,impliedMove,ieeEarnEffect,nextErn,absAvgErnMv"
url = f"https://api.orats.io/datav2/summaries?token={token}&ticker={ticker}&fields={fields}"

print("Requesting ex-earnings IV and implied move fields for AAPL...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
