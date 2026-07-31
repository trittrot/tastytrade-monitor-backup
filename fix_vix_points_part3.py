with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_calc = "pct_change = (price - open_price) / open_price * 100"
new_calc = "points_change = price - open_price"

if old_calc not in content:
    print("ERROR: calculation line not found")
else:
    content = content.replace(old_calc, new_calc)
    print("Calculation changed to raw points")

old_up_check = """if pct_change >= threshold and threshold not in fired_up:
                            msg = f"Tastytrade VIX ALERT: {UP_MESSAGES[threshold]} (now {price:.2f}, {pct_change:+.1f}%)"
                            print(msg)
                            send_alert(msg)
                            fired_up.add(threshold)
                        if pct_change <= -threshold and threshold not in fired_down:
                            msg = f"Tastytrade VIX ALERT: {DOWN_MESSAGES[threshold]} (now {price:.2f}, {pct_change:+.1f}%)"
                            print(msg)
                            send_alert(msg)
                            fired_down.add(threshold)"""

new_up_check = """if points_change >= threshold and threshold not in fired_up:
                            msg = f"Tastytrade VIX ALERT: {UP_MESSAGES[threshold]} (now {price:.2f}, {points_change:+.1f} pts)"
                            print(msg)
                            send_alert(msg)
                            fired_up.add(threshold)
                        if points_change <= -threshold and threshold not in fired_down:
                            msg = f"Tastytrade VIX ALERT: {DOWN_MESSAGES[threshold]} (now {price:.2f}, {points_change:+.1f} pts)"
                            print(msg)
                            send_alert(msg)
                            fired_down.add(threshold)"""

if old_up_check not in content:
    print("ERROR: threshold check block not found")
else:
    content = content.replace(old_up_check, new_up_check)
    print("Threshold check logic updated to points")

with open('vix_live_monitor.py', 'w') as f:
    f.write(content)
