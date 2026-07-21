import asyncio
import csv
import os
from datetime import date
from tastytrade import DXLinkStreamer
from tastytrade.dxfeed import Quote
from auth import authenticate_production
from alerts import send_alert

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'es_close_log.csv')

async def capture_es_close(session):
    data = session._get('/instruments/futures?product-code=ES')
    active_future = next(f for f in data['items'] if f.get('active-month'))
    symbol = active_future['streamer-symbol']

    async with DXLinkStreamer(session) as streamer:
        await streamer.subscribe(Quote, [symbol])
        q = await asyncio.wait_for(streamer.get_event(Quote), timeout=10)

    bid = float(q.bid_price) if q.bid_price else None
    ask = float(q.ask_price) if q.ask_price else None
    mid = (bid + ask) / 2

    today = date.today().isoformat()
    print(f"ES close capture ({today}): {symbol} mid={mid:.2f}")

    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'symbol', 'close_price'])
        writer.writerow([today, symbol, round(mid, 2)])

    return mid

if __name__ == "__main__":
    try:
        session = authenticate_production()
        asyncio.run(capture_es_close(session))
    except Exception as e:
        send_alert(f"Tastytrade monitor: ES close capture FAILED - {e}")
        raise
