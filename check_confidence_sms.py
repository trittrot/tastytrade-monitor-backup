import urllib.request
import json
import sys
from secrets_loader import get_secret
from alerts import send_alert

ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "SPY"

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/summaries?token={token}&ticker={ticker}&fields=ticker,confidence"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())['data'][0]

confidence = data['confidence']
msg = f"Tastytrade: {ticker} confidence = {round(confidence*100, 2)}%"
print(msg)
send_alert(msg)
