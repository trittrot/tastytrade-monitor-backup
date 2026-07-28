with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_import_line = "from datetime import date, datetime, timedelta"
new_functions = """from datetime import date, datetime, timedelta
import urllib.request
import csv
import io

def fetch_cboe_prior_close():
    url = "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv"
    with urllib.request.urlopen(url) as response:
        csv_text = response.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    last_row = rows[-1]
    return float(last_row['CLOSE']), last_row['DATE']
"""

if old_import_line not in content:
    print("ERROR: import line not found")
else:
    content = content.replace(old_import_line, new_functions, 1)
    with open('vix_live_monitor.py', 'w') as f:
        f.write(content)
    print("CBOE prior-close fetch function added")
