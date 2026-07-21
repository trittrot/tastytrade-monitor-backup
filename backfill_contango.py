import urllib.request
import json
import time
import csv
from datetime import date, timedelta
from secrets_loader import get_secret

token = get_secret('orats-api-token')
TICKER = 'SPY'

end = date.today() - timedelta(days=1)
start = end - timedelta(days=21)

results = []
current = start
while current <= end:
    if current.weekday() < 5:
        date_str = current.isoformat()
        url = f'https://api.orats.io/datav2/hist/cores?token={token}&ticker={TICKER}&tradeDate={date_str}&fields=tradeDate,contango'
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                if data.get('data'):
                    contango = data['data'][0]['contango']
                    results.append((date_str, contango))
                    print(date_str + ': ' + str(contango))
        except Exception as e:
            print(date_str + ': ERROR - ' + str(e))
        time.sleep(0.3)
    current += timedelta(days=1)

results = results[-15:]

with open('orats_contango_log.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'contango', 'pct_change'])
    prev_val = None
    for d, val in results:
        if prev_val is not None and prev_val != 0:
            pct = (val - prev_val) / abs(prev_val) * 100
        else:
            pct = ''
        writer.writerow([d, val, round(pct, 2) if pct != '' else ''])
        prev_val = val

print('Backfill complete - ' + str(len(results)) + ' days written')
