with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_block = """                    current_today = date.today().isoformat()
                    if current_today != today:
                        today = current_today
                        open_price = None
                        fired_up = set()
                        fired_down = set()
                        print(f"New trading day: {today} - thresholds reset")"""

new_block = """                    now_check = datetime.now()
                    reset_time = now_check.replace(hour=21, minute=15, second=0, microsecond=0)
                    current_reset_date = now_check.date().isoformat() if now_check >= reset_time else (now_check.date() - timedelta(days=1)).isoformat()
                    if current_reset_date != today:
                        today = current_reset_date
                        open_price = None
                        fired_up = set()
                        fired_down = set()
                        print(f"New reference cycle (post 21:15 UK): {today} - thresholds reset")"""

count = content.count(old_block)
print(f"Found {count} occurrence(s) of the old block")

if count == 0:
    print("ERROR: block not found, no changes made")
else:
    content = content.replace(old_block, new_block)
    if "timedelta" not in content.split("new_block")[0] and "from datetime import" in content:
        content = content.replace("from datetime import date, datetime", "from datetime import date, datetime, timedelta")
    with open('vix_live_monitor.py', 'w') as f:
        f.write(content)
    print("VIX monitor reference point changed to 21:15 UK reset")
