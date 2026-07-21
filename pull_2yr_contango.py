import urllib.request
import json
import time
import csv
from datetime import date, timedelta
from secrets_loader import get_secret

token = get_secret('orats-api-token')
TICKER = 'SPY'

end = date.today() - timedelta(days=1)
start = end - timedelta(days=730)

results = []
count = 0
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
        except Exception as e:
            pass
        count += 1
        if count % 25 == 0:
            print('Processed ' + str(count) + ' days, collected ' + str(len(results)) + ' readings, currently at ' + date_str)
        time.sleep(0.2)
    current += timedelta(days=1)

with open('contango_2yr_history.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'contango'])
    for d, val in results:
        writer.writerow([d, val])

print('DONE - Pulled ' + str(len(results)) + ' days of history')
