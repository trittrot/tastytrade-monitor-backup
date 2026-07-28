with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_block = """            session = authenticate_production()
            session_start = datetime.now()
            today = date.today().isoformat()
            open_price = None
            fired_up = set()
            fired_down = set()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Authenticated. Starting VIX live monitor for {today}")"""

new_block = """            session = authenticate_production()
            session_start = datetime.now()

            now_startup = datetime.now()
            reset_time_startup = now_startup.replace(hour=21, minute=15, second=0, microsecond=0)
            if now_startup >= reset_time_startup:
                today = now_startup.date().isoformat()
            else:
                today = (now_startup.date() - timedelta(days=1)).isoformat()

            try:
                open_price, cboe_date = fetch_cboe_prior_close()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Startup mid-cycle - using CBOE genuine prior close: {open_price} (dated {cboe_date})")
            except Exception as e:
                open_price = None
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Could not fetch CBOE prior close ({e}) - will use next live tick instead")

            fired_up = set()
            fired_down = set()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Authenticated. Starting VIX live monitor for {today}")"""

count = content.count(old_block)
print(f"Found {count} occurrence(s)")

if count == 0:
    print("ERROR: block not found, no changes made")
else:
    content = content.replace(old_block, new_block)
    with open('vix_live_monitor.py', 'w') as f:
        f.write(content)
    print("Startup now correctly fetches genuine CBOE prior close for mid-cycle joins")
