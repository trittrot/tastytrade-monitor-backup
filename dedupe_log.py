with open('orats_contango_log.csv', 'r') as f:
    rows = f.readlines()

header = rows[0]
data_rows = rows[1:]

seen_dates = set()
cleaned = []
for row in reversed(data_rows):
    d = row.split(',')[0]
    if d not in seen_dates:
        cleaned.append(row)
        seen_dates.add(d)

cleaned.reverse()

with open('orats_contango_log.csv', 'w') as f:
    f.write(header)
    f.writelines(cleaned)

print("Deduplicated - kept " + str(len(cleaned)) + " unique days")
