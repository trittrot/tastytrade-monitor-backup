with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_block = """            try:
                open_price, cboe_date = fetch_cboe_prior_close()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Startup mid-cycle - using CBOE prior close: {open_price} (dated {cboe_date})")
            except Exception as e:
                open_price = None
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Could not fetch CBOE prior close: {e}")"""

new_block = """            active_thresholds = None
            regime_name = None
            try:
                open_price, cboe_date = fetch_cboe_prior_close()
                active_thresholds, regime_name = get_regime_thresholds(open_price)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Startup mid-cycle - CBOE prior close: {open_price} (dated {cboe_date}) - Regime: {regime_name} - Thresholds: {active_thresholds}")
            except Exception as e:
                open_price = None
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Could not fetch CBOE prior close: {e}")"""

if old_block not in content:
    print("ERROR: block not found")
else:
    content = content.replace(old_block, new_block)
    with open('vix_live_monitor.py', 'w') as f:
        f.write(content)
    print("Startup path now correctly sets regime thresholds too")
