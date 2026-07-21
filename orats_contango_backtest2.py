import urllib.request
import json
import time
from datetime import date, timedelta
from secrets_loader import get_secret

token = get_secret("orats-api-token")
TICKER = "SPY"

start = date(2024, 7, 19)
end = date(2024, 8, 9)

results = []
current = start
while current <= end:
    if current.weekday() < 5:
        date_str = current.isoformat()
        url = f"https://api.orats.io/datav2/hist/cores?token={token}&ticker={TICKER}&tradeDate={date_str}&fields=tradeDate,contango"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                if data.get('data'):
                    contango = data['data'][0]['contango']
                    results.append((date_str, contango))
                    print(f"{date_str}: contango = {contango}")
                else:
                    print(f"{date_str}: no data (holiday?)")
        except Exception as e:
            print(f"{date_str}: ERROR - {e}")
        time.sleep(0.3)
    current += timedelta(days=1)

print("\n--- Day-over-day change ---")
for i in range(1, len(results)):
    prev_date, prev_val = results[i-1]
    curr_date, curr_val = results[i]
    if prev_val != 0:
        pct_change = (curr_val - prev_val) / abs(prev_val) * 100
    else:
        pct_change = float('inf')
    print(f"{prev_date} -> {curr_date}: {prev_val:+.4f} -> {curr_val:+.4f}  (change: {pct_change:+.1f}%)")
