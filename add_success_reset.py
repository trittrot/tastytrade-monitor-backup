with open('etf_iv_percentile_alert.py', 'r') as f:
    content = f.read()

old_line = "                iv_data = fetch_iv_data(symbols)"
new_line = "                iv_data = fetch_iv_data(symbols)\n                failure_alerted_today = False"

if old_line not in content:
    print("ERROR: line not found")
else:
    content = content.replace(old_line, new_line, 1)
    with open('etf_iv_percentile_alert.py', 'w') as f:
        f.write(content)
    print("Success reset added - failure flag clears after a genuinely successful check")
