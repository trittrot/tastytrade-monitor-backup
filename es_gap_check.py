import asyncio
import csv
import os
from datetime import date
from tastytrade import DXLinkStreamer
from tastytrade.dxfeed import Quote
from auth import authenticate_production
from alerts import send_alert

CLOSE_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'es_close_log.csv')
GAP_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'es_gap_log.csv')
THRESHOLD_PCT = 0.5

def get_last_close():
    if not os.path.exists(CLOSE_LOG):
        return None
    with open(CLOSE_LOG, 'r') as f:
        rows = list(csv.reader(f))
    if len(rows) < 2:
        return None
    last_row = rows[-1]
    return float(last_row[2])

async def check_es_gap(session):
    last_close = get_last_close()
    if last_close is None:
        print("No previous close on record - skipping gap check")
        send_alert("Tastytrade monitor: ES gap check - no previous close on record yet")
        return None

    data = session._get('/instruments/futures?product-code=ES')
    active_future = next(f for f in data['items'] if f.get('active-month'))
    symbol = active_future['streamer-symbol']

    async with DXLinkStreamer(session) as streamer:
        await streamer.subscribe(Quote, [symbol])
        q = await asyncio.wait_for(streamer.get_event(Quote), timeout=10)

    bid = float(q.bid_price) if q.bid_price else None
    ask = float(q.ask_price) if q.ask_price else None
    current_price = (bid + ask) / 2

    gap_points = current_price - last_close
    gap_pct = (gap_points / last_close) * 100
    direction = "GAP UP" if gap_points > 0 else "GAP DOWN" if gap_points < 0 else "FLAT"

    today = date.today().isoformat()
    print(f"ES Gap Check ({today}): Last close={last_close:.2f}  Current={current_price:.2f}")
    print(f"{direction}: {gap_points:+.2f} points ({gap_pct:+.2f}%)")

    file_exists = os.path.exists(GAP_LOG)
    with open(GAP_LOG, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'last_close', 'current_price', 'gap_points', 'gap_pct'])
        writer.writerow([today, last_close, round(current_price, 2), round(gap_points, 2), round(gap_pct, 4)])

    if abs(gap_pct) >= THRESHOLD_PCT:
        msg = f"Tastytrade ALERT: ES spot {current_price:.2f} - {direction} {gap_points:+.2f} pts ({gap_pct:+.2f}%) at London open"
    else:
        msg = f"Tastytrade: ES spot {current_price:.2f} - {direction} {gap_points:+.2f} pts ({gap_pct:+.2f}%) at London open - routine"

    print(msg)
    send_alert(msg)

    return gap_pct

if __name__ == "__main__":
    try:
        session = authenticate_production()
        asyncio.run(check_es_gap(session))
    except Exception as e:
        send_alert(f"Tastytrade monitor: ES gap check FAILED - {e}")
        raise
