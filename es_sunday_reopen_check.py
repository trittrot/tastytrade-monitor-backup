import asyncio
import csv
import os
from datetime import date
from tastytrade import DXLinkStreamer
from tastytrade.dxfeed import Quote
from auth import authenticate_production
from alerts import send_alert

CLOSE_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'es_close_log.csv')
THRESHOLD_PCT = 0.5

def get_last_close():
    if not os.path.exists(CLOSE_LOG):
        return None
    with open(CLOSE_LOG, 'r') as f:
        rows = list(csv.reader(f))
    if len(rows) < 2:
        return None
    return float(rows[-1][2])

async def check_sunday_reopen(session):
    friday_close = get_last_close()
    if friday_close is None:
        print("No previous close on record - skipping Sunday reopen check")
        send_alert("Tastytrade monitor: Sunday reopen check - no previous close on record")
        return None

    data = session._get('/instruments/futures?product-code=ES')
    active_future = next(f for f in data['items'] if f.get('active-month'))
    symbol = active_future['streamer-symbol']

    async with DXLinkStreamer(session) as streamer:
        await streamer.subscribe(Quote, [symbol])
        q = await asyncio.wait_for(streamer.get_event(Quote), timeout=10)

    bid = float(q.bid_price) if q.bid_price else None
    ask = float(q.ask_price) if q.ask_price else None
    reopen_price = (bid + ask) / 2

    gap_points = reopen_price - friday_close
    gap_pct = (gap_points / friday_close) * 100
    direction = "GAP UP" if gap_points > 0 else "GAP DOWN" if gap_points < 0 else "FLAT"

    today = date.today().isoformat()
    print(f"Sunday Reopen Check ({today}): Friday close={friday_close:.2f}  Reopen={reopen_price:.2f}")
    print(f"{direction}: {gap_points:+.2f} points ({gap_pct:+.2f}%)")

    file_exists = os.path.exists(CLOSE_LOG)
    with open(CLOSE_LOG, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'symbol', 'close_price'])
        writer.writerow([today, symbol, round(reopen_price, 2)])

    if abs(gap_pct) >= THRESHOLD_PCT:
        msg = f"Tastytrade ALERT: ES spot {reopen_price:.2f} - Sunday reopen {direction} {gap_pct:+.2f}% ({gap_points:+.2f} pts) vs Friday close"
    else:
        msg = f"Tastytrade: ES spot {reopen_price:.2f} - Sunday reopen {direction} {gap_pct:+.2f}% ({gap_points:+.2f} pts) vs Friday close - routine"

    print(msg)
    send_alert(msg)

    return gap_pct

if __name__ == "__main__":
    try:
        session = authenticate_production()
        asyncio.run(check_sunday_reopen(session))
    except Exception as e:
        send_alert(f"Tastytrade monitor: Sunday reopen check FAILED - {e}")
        raise
