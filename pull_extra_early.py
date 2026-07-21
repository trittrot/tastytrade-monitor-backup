import urllib.request
import json
import time
import csv
from datetime import date, timedelta
from secrets_loader import get_secret

token = get_secret('orats-api-token')
TICKER = 'SPY'

end = date(2024, 7, 18)
start = end - timedelta(days=20)

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
            print(date_str + ': ERROR')
        time.sleep(0.2)
    current += timedelta(days=1)

with open('contango_extra_early.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'contango'])
    for d, val in results:
        writer.writerow([d, val])

print('Pulled ' + str(len(results)) + ' extra days')
