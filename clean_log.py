with open('orats_contango_log.csv', 'r') as f:
    rows = f.readlines()

header = rows[0]
last_row = rows[-1]

with open('orats_contango_log.csv', 'w') as f:
    f.write(header)
    f.write(last_row)

print("Log cleaned - kept header and most recent row only")
