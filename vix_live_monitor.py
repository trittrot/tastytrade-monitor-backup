import asyncio
import time
from datetime import date, datetime, timedelta
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

from tastytrade import DXLinkStreamer
from tastytrade.dxfeed import Trade
from auth import authenticate_production
from alerts import send_alert

THRESHOLDS = [10, 15, 20, 25, 30]
REAUTH_INTERVAL_HOURS = 4

UP_MESSAGES = {
    10: "VIX +10% from open - review existing short premium positions",
    15: "VIX +15% from open - consider adjustments to short premium positions",
    20: "VIX +20% from open - consider new short premium entries (check ORATS)",
    25: "VIX +25% from open - significant vol event, scan ORATS for opportunities",
    30: "VIX +30% from open - major vol event, review book thoroughly",
}

DOWN_MESSAGES = {
    10: "VIX -10% from open - vol cooling, monitor long premium positions",
    15: "VIX -15% from open - review long premium/hedge positions",
    20: "VIX -20% from open - consider whether long hedge still needed",
    25: "VIX -25% from open - significant vol collapse, reassess hedge",
    30: "VIX -30% from open - major vol collapse, review hedge urgently",
}

async def run_vix_monitor():
    while True:
        try:
            session = authenticate_production()
            session_start = datetime.now()
            now_startup = datetime.now()
            reset_time_startup = now_startup.replace(hour=21, minute=15, second=0, microsecond=0)
            if now_startup >= reset_time_startup:
                today = now_startup.date().isoformat()
            else:
                today = (now_startup.date() - timedelta(days=1)).isoformat()
            try:
                open_price, cboe_date = fetch_cboe_prior_close()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Startup mid-cycle - using CBOE prior close: {open_price} (dated {cboe_date})")
            except Exception as e:
                open_price = None
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Could not fetch CBOE prior close: {e}")
            fired_up = set()
            fired_down = set()

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Authenticated. Starting VIX live monitor for {today}")

            async with DXLinkStreamer(session) as streamer:
                await streamer.subscribe(Trade, ['VIX'])

                while True:
                    if datetime.now() - session_start > timedelta(hours=REAUTH_INTERVAL_HOURS):
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Scheduled re-authentication ({REAUTH_INTERVAL_HOURS}h elapsed)")
                        break

                    now_check = datetime.now()
                    reset_time = now_check.replace(hour=21, minute=15, second=0, microsecond=0)
                    current_reset_date = now_check.date().isoformat() if now_check >= reset_time else (now_check.date() - timedelta(days=1)).isoformat()
                    if current_reset_date != today:
                        today = current_reset_date
                        open_price = None
                        fired_up = set()
                        fired_down = set()
                        print(f"New reference cycle (post 21:15 UK): {today} - thresholds reset")

                    try:
                        t = await asyncio.wait_for(streamer.get_event(Trade), timeout=30)
                        price = float(t.price)
                    except asyncio.TimeoutError:
                        continue

                    if open_price is None:
                        open_price = price
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Reference (open) price set: {open_price}")
                        continue

                    pct_change = (price - open_price) / open_price * 100

                    for threshold in sorted(THRESHOLDS, reverse=True):
                        if pct_change >= threshold and threshold not in fired_up:
                            msg = f"Tastytrade VIX ALERT: {UP_MESSAGES[threshold]} (now {price:.2f}, {pct_change:+.1f}%)"
                            print(msg)
                            send_alert(msg)
                            fired_up.add(threshold)
                        if pct_change <= -threshold and threshold not in fired_down:
                            msg = f"Tastytrade VIX ALERT: {DOWN_MESSAGES[threshold]} (now {price:.2f}, {pct_change:+.1f}%)"
                            print(msg)
                            send_alert(msg)
                            fired_down.add(threshold)

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e} - reconnecting in 10s")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run_vix_monitor())
