import asyncio
import sys
from tastytrade import DXLinkStreamer
from tastytrade.dxfeed import Quote
from auth import authenticate_production

ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "SPY"

async def check_price():
    session = authenticate_production()
    async with DXLinkStreamer(session) as streamer:
        await streamer.subscribe(Quote, [ticker])
        q = await asyncio.wait_for(streamer.get_event(Quote), timeout=10)

    bid = float(q.bid_price) if q.bid_price else None
    ask = float(q.ask_price) if q.ask_price else None
    mid = (bid + ask) / 2 if bid and ask else None

    print(f"=== {ticker} Live Price ===")
    print(f"Bid: {bid}  Ask: {ask}  Mid: {mid}")

asyncio.run(check_price())
