import csv
import os

QUALIFYING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etf_qualifying_symbols.csv')

if not os.path.exists(QUALIFYING_PATH):
    print("No scan data yet - the scanner may not have run during cash market hours yet today.")
else:
    with open(QUALIFYING_PATH, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Scan file exists but is empty.")
    else:
        print(f"ETF Confidence Scan - last updated: {rows[0]['updated_at']}")
        print(f"{len(rows)} symbols currently qualify (confidence > 90%):")
        print()
        for row in sorted(rows, key=lambda r: float(r['confidence']), reverse=True):
            print(f"  {row['symbol']:6s}  {float(row['confidence'])*100:.2f}%")
