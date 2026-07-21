import csv

with open('contango_2yr_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = [(r['date'], float(r['contango'])) for r in reader]

target_date = '2024-07-24'
idx = None
for i, (d, v) in enumerate(rows):
    if d == target_date:
        idx = i
        break

if idx is None or idx < 10:
    print('Not enough prior data or date not found')
else:
    window = [rows[j][1] for j in range(idx-10, idx)]
    ma = sum(window) / len(window)
    today_val = rows[idx][1]
    dev = today_val - ma
    print('Date: ' + target_date)
    print('Prior 10 days: ' + str([round(w,3) for w in window]))
    print('10-day MA: ' + str(round(ma,4)))
    print('Actual value: ' + str(today_val))
    print('Deviation: ' + str(round(dev,4)) + ' points')
