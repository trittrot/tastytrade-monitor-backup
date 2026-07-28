with open('es_iv_live_monitor.py', 'r') as f:
    content = f.read()

old_line = "                        already_alerted = True"
new_lines = """                        already_alerted = True

                    if iv_pctile > THRESHOLD_HIGH and not already_alerted_high:
                        sms_msg_high = 'Tastytrade ALERT: ES IV Percentile ' + str(round(iv_pctile,1)) + '% exceeds ' + str(THRESHOLD_HIGH) + '% HIGH threshold. IV Rank: ' + str(round(iv_rank,1)) + '%'
                        send_alert(sms_msg_high)
                        already_alerted_high = True
                    elif iv_pctile <= THRESHOLD_HIGH and already_alerted_high:
                        already_alerted_high = False"""

count = content.count(old_line)
print(f"Found {count} occurrence(s) of target line")

if count == 0:
    print("ERROR: line not found")
elif count > 1:
    print("ERROR: multiple matches, need unique target")
else:
    content = content.replace(old_line, new_lines)
    with open('es_iv_live_monitor.py', 'w') as f:
        f.write(content)
    print("90% threshold tier added successfully")
