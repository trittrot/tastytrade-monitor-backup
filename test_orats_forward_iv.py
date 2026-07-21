import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
ticker = "SPY"
fields = "ticker,tradeDate,fwd30_20,fwd90_30,ffwd30_20,ffwd90_30,fbfwd30_20,fbfwd90_30"
url = f"https://api.orats.io/datav2/summaries?token={token}&ticker={ticker}&fields={fields}"

print("Requesting Forward and Flat Forward IV fields for SPY...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
