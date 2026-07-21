import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
ticker = "SPY"

summaries_fields = "ticker,tradeDate,exErnIv10d,exErnIv20d,exErnIv30d,exErnIv60d,exErnIv90d,exErnIv6m,exErnIv1y,contango,fwd30_20,fwd60_30,fwd90_60,fwd180_90,fwd90_30,fbfwd30_20,fbfwd60_30,fbfwd90_60,fbfwd180_90,fbfwd90_30,confidence,iv30d,rSlp30"
url1 = f"https://api.orats.io/datav2/summaries?token={token}&ticker={ticker}&fields={summaries_fields}"

cores_fields = "ticker,tradeDate,slope,slopeInf,slopeFcst,slopeFcstInf,slopepctile,ivPctile1y,ivHvXernRatio,orHvXern20d,deriv,derivInf"
url2 = f"https://api.orats.io/datav2/cores?token={token}&ticker={ticker}&fields={cores_fields}"

print("=== SUMMARIES ===")
with urllib.request.urlopen(url1) as response:
    print(json.dumps(json.loads(response.read()), indent=2))

print("\n=== CORES ===")
with urllib.request.urlopen(url2) as response:
    print(json.dumps(json.loads(response.read()), indent=2))
