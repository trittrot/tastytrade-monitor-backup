import urllib.request
import json
import sys
from datetime import datetime
from secrets_loader import get_secret

ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "SPY"

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/cores?token={token}&ticker={ticker}&fields=ticker,tradeDate,contango"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())['data'][0]

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"=== Contango Check - {ticker} ===")
print(f"UK time now:      {now}")
print(f"ORATS tradeDate:  {data['tradeDate']}")
print(f"Contango value:   {data['contango']}")
