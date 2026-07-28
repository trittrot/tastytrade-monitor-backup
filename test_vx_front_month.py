import asyncio
from tastytrade import DXLinkStreamer
from tastytrade.dxfeed import Quote
from auth import authenticate_production

async def check_vx_front_month():
    session = authenticate_production()
    data = session._get('/instruments/futures?product-code=VX')
    active_future = next(f for f in data['items'] if f.get('active-month'))
    symbol = active_future['streamer-symbol']
    print(f"Front month /VX contract: {symbol}")

    async with DXLinkStreamer(session) as streamer:
        await streamer.subscribe(Quote, [symbol])
        q = await asyncio.wait_for(streamer.get_event(Quote), timeout=10)

    bid = float(q.bid_price) if q.bid_price else None
    ask = float(q.ask_price) if q.ask_price else None
    mid = (bid + ask) / 2 if bid and ask else None
    print(f"Bid: {bid}  Ask: {ask}  Mid: {mid}")

asyncio.run(check_vx_front_month())
