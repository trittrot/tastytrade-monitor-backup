import urllib.request
import json
from datetime import datetime
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/cores?token={token}&ticker=SPY&fields=ticker,tradeDate,contango"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())['data'][0]

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"=== Contango Check ===")
print(f"UK time now:      {now}")
print(f"ORATS tradeDate:  {data['tradeDate']}")
print(f"Contango value:   {data['contango']}")
