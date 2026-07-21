import csv

LOCAL = "VIX_History.csv"

up_moves = []
down_moves = []

with open(LOCAL, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            o = float(row['OPEN'])
            h = float(row['HIGH'])
            l = float(row['LOW'])
        except (ValueError, KeyError):
            continue
        if o <= 0:
            continue
        up_moves.append((h - o) / o * 100)
        down_moves.append((l - o) / o * 100)

n = len(up_moves)

with open("threshold_results.txt", "w") as out:
    out.write(f"Total days analysed: {n}\n\n")
    for threshold in [10, 15, 20, 25, 30]:
        up_count = sum(1 for x in up_moves if x >= threshold)
        down_count = sum(1 for x in down_moves if x <= -threshold)
        up_pct = up_count / n * 100
        down_pct = down_count / n * 100
        up_freq_days = n / up_count if up_count > 0 else float('inf')
        down_freq_days = n / down_count if down_count > 0 else float('inf')
        out.write(f"Threshold {threshold} percent\n")
        out.write(f"  UP >= {threshold}%: {up_count} days ({up_pct:.2f}%) - roughly every {up_freq_days:.0f} trading days\n")
        out.write(f"  DOWN <= -{threshold}%: {down_count} days ({down_pct:.2f}%) - roughly every {down_freq_days:.0f} trading days\n\n")

print("Done - results written to threshold_results.txt")
