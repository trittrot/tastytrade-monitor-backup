import asyncio
from datetime import datetime
from tastytrade import DXLinkStreamer
from tastytrade.dxfeed import Trade, Quote
from auth import authenticate_production

async def check_vix(session):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Checking VIX at {now} (local VM time, UK)")

    async with DXLinkStreamer(session) as streamer:
        await streamer.subscribe(Trade, ['VIX'])
        await streamer.subscribe(Quote, ['VIX'])

        trade_result = None
        quote_result = None

        try:
            for _ in range(2):
                event = await asyncio.wait_for(streamer.get_event(Trade), timeout=8)
                trade_result = event
                break
        except asyncio.TimeoutError:
            print("No Trade event received (timeout)")

        try:
            for _ in range(2):
                event = await asyncio.wait_for(streamer.get_event(Quote), timeout=8)
                quote_result = event
                break
        except asyncio.TimeoutError:
            print("No Quote event received (timeout)")

    if trade_result:
        print(f"Trade: price={trade_result.price}  time={trade_result.time}")
    else:
        print("Trade: no data")

    if quote_result:
        print(f"Quote: bid={quote_result.bid_price}  ask={quote_result.ask_price}")
    else:
        print("Quote: no data")

if __name__ == "__main__":
    session = authenticate_production()
    asyncio.run(check_vix(session))
