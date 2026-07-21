import csv
import os
import asyncio
from datetime import date
from tastytrade.dxfeed import Trade
from tastytrade import DXLinkStreamer
from auth import authenticate_production
from alerts import send_alert

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contango_log.csv')

def get_previous_ratio(log_path, today):
    if not os.path.exists(log_path):
        return None
    with open(log_path, 'r') as f:
        rows = list(csv.reader(f))
    for row in reversed(rows[1:]):
        if row[0] != today:
            return float(row[3])
    return None

async def record_and_compare_contango(session):
    async with DXLinkStreamer(session) as streamer:
        await streamer.subscribe(Trade, ['VIX', 'VIX3M'])
        results = {}
        try:
            for _ in range(2):
                t = await asyncio.wait_for(streamer.get_event(Trade), timeout=10)
                results[t.event_symbol] = float(t.price)
        except asyncio.TimeoutError:
            pass

    if 'VIX' not in results or 'VIX3M' not in results:
        print("Failed to get both readings - aborting")
        send_alert("Tastytrade monitor: contango check FAILED to get VIX/VIX3M data")
        return None

    vix = results['VIX']
    vix3m = results['VIX3M']
    ratio = (vix3m - vix) / vix * 100
    today = date.today().isoformat()

    print(f"Today ({today}): VIX={vix:.2f}  VIX3M={vix3m:.2f}  Ratio={ratio:+.2f}%")

    previous_ratio = get_previous_ratio(LOG_PATH, today)

    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'vix', 'vix3m', 'ratio_pct'])
        writer.writerow([today, vix, vix3m, round(ratio, 4)])

    if previous_ratio is not None:
        change = ratio - previous_ratio
        sign_flip = (previous_ratio > 0 and ratio < 0) or (previous_ratio < 0 and ratio > 0)
        print(f"Previous ratio: {previous_ratio:+.2f}%  |  Change: {change:+.2f} percentage points")
        if sign_flip:
            msg = f"Tastytrade ALERT: Contango sign FLIP. Was {previous_ratio:+.2f}%, now {ratio:+.2f}%"
            print(msg)
            send_alert(msg)
        else:
            print(f"No alert - change of {change:+.2f} points (logging only, threshold not yet calibrated)")
    else:
        print("No previous entry to compare against yet")

    return ratio

if __name__ == "__main__":
    session = authenticate_production()
    asyncio.run(record_and_compare_contango(session))
