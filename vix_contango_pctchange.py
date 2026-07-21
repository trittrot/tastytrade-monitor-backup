import csv

ratios = []
with open("contango_history.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ratios.append((row['date'], float(row['ratio_pct'])))

pct_changes = []
skipped_near_zero = 0

for i in range(1, len(ratios)):
    prev_date, prev = ratios[i-1]
    curr_date, curr = ratios[i]
    if abs(prev) < 1.0:
        skipped_near_zero += 1
        continue
    pct_change = (curr - prev) / abs(prev) * 100
    pct_changes.append((curr_date, prev, curr, pct_change))

print(f"Total transitions: {len(ratios)-1}")
print(f"Skipped (previous day ratio near zero, <1%, unstable): {skipped_near_zero}")
print(f"Usable transitions: {len(pct_changes)}")

abs_changes = sorted(abs(x[3]) for x in pct_changes)
n = len(abs_changes)
print(f"\n--- Relative day-to-day % change in contango ratio ---")
print(f"Median: {abs_changes[n//2]:.1f}%")
print(f"90th pct: {abs_changes[int(n*0.9)]:.1f}%")
print(f"95th pct: {abs_changes[int(n*0.95)]:.1f}%")
print(f"99th pct: {abs_changes[int(n*0.99)]:.1f}%")
print(f"Max: {abs_changes[-1]:.1f}%")

print(f"\n--- Days with relative change >= 50% ---")
big_moves = [x for x in pct_changes if abs(x[3]) >= 50]
print(f"Count: {len(big_moves)} ({len(big_moves)/len(pct_changes)*100:.2f}% of days)")

print(f"\n--- Days with relative change >= 100% ---")
huge_moves = [x for x in pct_changes if abs(x[3]) >= 100]
print(f"Count: {len(huge_moves)} ({len(huge_moves)/len(pct_changes)*100:.2f}% of days)")

print(f"\n--- Most recent 15 days with relative change >= 50% ---")
for d, prev, curr, pct in big_moves[-15:]:
    print(f"  {d}: {prev:+.2f}% -> {curr:+.2f}%  (relative change {pct:+.1f}%)")
