with open('vix_live_monitor.py', 'r') as f:
    content = f.read()

old_block = """                    if open_price is None:
                        open_price = price
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Reference (open) price set: {open_price}")
                        continue
                    points_change = price - open_price
                    for threshold in sorted(THRESHOLDS, reverse=True):"""

new_block = """                    if open_price is None:
                        open_price = price
                        active_thresholds, regime_name = get_regime_thresholds(open_price)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Reference (open) price set: {open_price} - regime: {regime_name}, thresholds: {active_thresholds}")
                        continue
                    points_change = price - open_price
                    for threshold in sorted(active_thresholds, reverse=True):"""

if old_block not in content:
    print("ERROR: block not found")
else:
    content = content.replace(old_block, new_block)
    with open('vix_live_monitor.py', 'w') as f:
        f.write(content)
    print("Regime thresholds now actively used in main loop")
