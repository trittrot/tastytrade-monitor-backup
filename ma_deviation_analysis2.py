import csv

with open('contango_2yr_history.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = [(r['date'], float(r['contango'])) for r in reader]

deviations = []
for i in range(10, len(rows)):
    window = [rows[j][1] for j in range(i-10, i)]
    ma = sum(window) / len(window)
    today_val = rows[i][1]
    dev = today_val - ma
    deviations.append((rows[i][0], dev, ma, today_val))

abs_devs = sorted(abs(d[1]) for d in deviations)
n = len(abs_devs)

print('Total days analysed: ' + str(n))
print('Median absolute deviation: ' + str(round(abs_devs[n//2],3)) + ' points')
print('90th percentile: ' + str(round(abs_devs[int(n*0.9)],3)) + ' points')
print('95th percentile: ' + str(round(abs_devs[int(n*0.95)],3)) + ' points')
print('99th percentile: ' + str(round(abs_devs[int(n*0.99)],3)) + ' points')
print('Max: ' + str(round(abs_devs[-1],3)) + ' points')

with open('ma_deviation_history2.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'deviation_points', 'ma', 'today_val'])
    for d, dev, ma, val in deviations:
        writer.writerow([d, round(dev,4), round(ma,4), val])

print('Saved to ma_deviation_history2.csv')
