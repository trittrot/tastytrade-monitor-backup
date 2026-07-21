import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
ticker = "SPY"
fields = "ticker,tradeDate,rSlp30,rSlp2y,slopepctile,slopeavg1m,slopeavg1y,slopeStdv1y,etfSlopeRatio,etfSlopeRatioAvg1m,etfSlopeRatioAvg1y"
url = f"https://api.orats.io/datav2/summaries?token={token}&ticker={ticker}&fields={fields}"

print("Requesting SMV Summaries slope percentile family for SPY...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
