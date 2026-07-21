import csv

rows = []
with open('contango_extra_early.csv', 'r') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append((r['date'], float(r['contango'])))

with open('contango_2yr_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append((r['date'], float(r['contango'])))

rows.sort(key=lambda x: x[0])

seen = set()
deduped = []
for d, v in rows:
    if d not in seen:
        deduped.append((d, v))
        seen.add(d)

with open('contango_merged.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'contango'])
    for d, v in deduped:
        writer.writerow([d, v])

target_date = '2024-07-24'
idx = None
for i, (d, v) in enumerate(deduped):
    if d == target_date:
        idx = i
        break

if idx is None or idx < 10:
    print('Still not enough data')
else:
    window = [deduped[j][1] for j in range(idx-10, idx)]
    ma = sum(window) / len(window)
    today_val = deduped[idx][1]
    dev = today_val - ma
    print('Date: ' + target_date)
    print('Prior 10 days: ' + str([round(w,3) for w in window]))
    print('10-day MA: ' + str(round(ma,4)))
    print('Actual value: ' + str(today_val))
    print('Deviation: ' + str(round(dev,4)) + ' points')
