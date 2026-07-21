import csv

with open('contango_2yr_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = [(r['date'], float(r['contango'])) for r in reader]

deviations = []
for i in range(10, len(rows)):
    window = [rows[j][1] for j in range(i-10, i)]
    ma = sum(window) / len(window)
    today_val = rows[i][1]
    if ma != 0:
        dev = (today_val - ma) / abs(ma) * 100
        deviations.append((rows[i][0], dev))

abs_devs = sorted(abs(d[1]) for d in deviations)
n = len(abs_devs)

print('Total days analysed: ' + str(n))
print('Median deviation: ' + str(round(abs_devs[n//2],1)) + ' percent')
print('90th percentile: ' + str(round(abs_devs[int(n*0.9)],1)) + ' percent')
print('95th percentile: ' + str(round(abs_devs[int(n*0.95)],1)) + ' percent')
print('99th percentile: ' + str(round(abs_devs[int(n*0.99)],1)) + ' percent')
print('Max: ' + str(round(abs_devs[-1],1)) + ' percent')

with open('ma_deviation_history.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'deviation_pct'])
    for d, dev in deviations:
        writer.writerow([d, round(dev,2)])

print('Saved full deviation history to ma_deviation_history.csv')
