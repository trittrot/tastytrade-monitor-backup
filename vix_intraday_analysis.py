import csv
import urllib.request
from statistics import quantiles

URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"
LOCAL = "VIX_History.csv"

print("Downloading VIX history from CBOE...")
urllib.request.urlretrieve(URL, LOCAL)

up_moves = []
down_moves = []
ranges = []
dates_up15 = []
dates_down15 = []

with open(LOCAL, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            o = float(row['OPEN'])
            h = float(row['HIGH'])
            l = float(row['LOW'])
            d = row['DATE']
        except (ValueError, KeyError):
            continue
        if o <= 0:
            continue
        up = (h - o) / o * 100
        down = (l - o) / o * 100
        rng = (h - l) / o * 100
        up_moves.append(up)
        down_moves.append(down)
        ranges.append(rng)
        if up >= 15:
            dates_up15.append((d, round(up, 1)))
        if down <= -15:
            dates_down15.append((d, round(down, 1)))

n = len(up_moves)
print(f"\nDays analysed: {n}")

print(f"\n--- Intraday UP move (high vs open, %) ---")
q = quantiles(up_moves, n=100)
print(f"Median: {q[49]:.2f}%  |  90th pct: {q[89]:.2f}%  |  95th: {q[94]:.2f}%  |  99th: {q[98]:.2f}%")
print(f"Days with +15% or more intraday: {len(dates_up15)} ({len(dates_up15)/n*100:.2f}% of days)")

print(f"\n--- Intraday DOWN move (low vs open, %) ---")
qd = quantiles([abs(x) for x in down_moves], n=100)
print(f"Median: {qd[49]:.2f}%  |  90th pct: {qd[89]:.2f}%  |  95th: {qd[94]:.2f}%  |  99th: {qd[98]:.2f}%")
print(f"Days with -15% or more intraday: {len(dates_down15)} ({len(dates_down15)/n*100:.2f}% of days)")

print(f"\n--- Most recent +15% intraday days ---")
for d, v in dates_up15[-10:]:
    print(f"  {d}: +{v}%")

print(f"\n--- Most recent -15% intraday days ---")
for d, v in dates_down15[-10:]:
    print(f"  {d}: {v}%")
