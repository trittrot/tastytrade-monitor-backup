import csv
import urllib.request
from datetime import datetime

VIX_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"
VIX3M_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv"

print("Downloading VIX and VIX3M history from CBOE...")
urllib.request.urlretrieve(VIX_URL, "VIX_History.csv")
urllib.request.urlretrieve(VIX3M_URL, "VIX3M_History.csv")

def load_closes(path):
    closes = {}
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                d = datetime.strptime(row['DATE'], '%m/%d/%Y').date()
                c = float(row['CLOSE'])
                closes[d] = c
            except (ValueError, KeyError):
                continue
    return closes

vix = load_closes("VIX_History.csv")
vix3m = load_closes("VIX3M_History.csv")

common_dates = sorted(set(vix.keys()) & set(vix3m.keys()))
print(f"Common trading days: {len(common_dates)}")
print(f"Date range: {common_dates[0]} to {common_dates[-1]}")

ratios = []
with open("contango_history.csv", "w", newline='') as out:
    writer = csv.writer(out)
    writer.writerow(['date', 'vix', 'vix3m', 'ratio_pct'])
    for d in common_dates:
        v = vix[d]
        v3 = vix3m[d]
        if v <= 0:
            continue
        ratio_pct = (v3 - v) / v * 100
        ratios.append((d, ratio_pct))
        writer.writerow([d.isoformat(), v, v3, round(ratio_pct, 4)])

backwardation_days = [r for r in ratios if r[1] < 0]
contango_days = [r for r in ratios if r[1] >= 0]

print(f"\nTotal days: {len(ratios)}")
print(f"Contango days (VIX3M > VIX): {len(contango_days)} ({len(contango_days)/len(ratios)*100:.2f}%)")
print(f"Backwardation days (VIX > VIX3M): {len(backwardation_days)} ({len(backwardation_days)/len(ratios)*100:.2f}%)")

print(f"\n--- Most recent backwardation days (true chronological order) ---")
for d, r in backwardation_days[-15:]:
    print(f"  {d}: {r:+.2f}%")

print(f"\n--- Sign-flip frequency (day-to-day, true chronological order) ---")
flips = 0
for i in range(1, len(ratios)):
    prev = ratios[i-1][1]
    curr = ratios[i][1]
    if (prev >= 0 and curr < 0) or (prev < 0 and curr >= 0):
        flips += 1
print(f"Sign flips: {flips} out of {len(ratios)-1} day-transitions ({flips/(len(ratios)-1)*100:.2f}%)")

print(f"\n--- Day-to-day change distribution (percentage points) ---")
changes_abs = sorted(abs(ratios[i][1] - ratios[i-1][1]) for i in range(1, len(ratios)))
n = len(changes_abs)
print(f"Median: {changes_abs[n//2]:.2f}")
print(f"90th pct: {changes_abs[int(n*0.9)]:.2f}")
print(f"95th pct: {changes_abs[int(n*0.95)]:.2f}")
print(f"99th pct: {changes_abs[int(n*0.99)]:.2f}")
