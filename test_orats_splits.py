import urllib.request
import json
from secrets_loader import get_secret

token = get_secret("orats-api-token")
url = f"https://api.orats.io/datav2/hist/splits?token={token}&ticker=AAPL"

print("Requesting ORATS Stock Split History for AAPL...")
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print("Response body:", e.read().decode())
