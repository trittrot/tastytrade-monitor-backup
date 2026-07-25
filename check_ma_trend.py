import urllib.request
import json
from datetime import date, timedelta
from secrets_loader import get_secret

def fetch_daily_prices(ticker='SPY', days_back=420):
    token = get_secret('orats-api-token')
    end = date.today()
    start = end - timedelta(days=days_back)
    prices = []
    current = start
    count = 0
    while current <= end:
        if current.weekday() < 5:
            date_str = current.isoformat()
            url = f'https://api.orats.io/datav2/hist/dailies?token={token}&ticker={ticker}&tradeDate={date_str}'
            try:
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read())
                    if data.get('data'):
                        clsPx = data['data'][0].get('clsPx')
                        if clsPx:
                            prices.append((date_str, clsPx))
            except Exception as e:
                print('Failed for ' + date_str + ': ' + str(e))
                pass
            count += 1
            if count % 50 == 0:
                print('Fetched ' + str(count) + ' days so far, at ' + date_str)
        current += timedelta(days=1)
    return prices

def calculate_moving_averages(prices):
    closes = [p[1] for p in prices]
    latest_date, latest_price = prices[-1]

    ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
    ma50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else None
    ma100 = sum(closes[-100:]) / 100 if len(closes) >= 100 else None

    return latest_date, latest_price, ma20, ma50, ma100

def determine_trend(price, ma20, ma50, ma100):
    if None in (ma20, ma50, ma100):
        return 'INSUFFICIENT DATA - not enough history for 100 day average'
    if price > ma20 and price > ma50 and price > ma100:
        return 'BULLISH - price above 20d, 50d, and 100d moving averages'
    elif price < ma20 and price < ma50 and price < ma100:
        return 'BEARISH - price below 20d, 50d, and 100d moving averages'
    else:
        return 'NEUTRAL - price mixed relative to moving averages, no clear trend alignment'

if __name__ == '__main__':
    print('Fetching SPY daily price history, this will take a few minutes...')
    prices = fetch_daily_prices('SPY', 280)
    print('Total trading days fetched: ' + str(len(prices)))

    latest_date, latest_price, ma20, ma50, ma100 = calculate_moving_averages(prices)

    print()
    print('=== SPY Trend Determination - ' + latest_date + ' ===')
    print('Latest close: ' + str(latest_price))
    print('20 day MA: ' + str(round(ma20,2) if ma20 else 'N/A'))
    print('50 day MA: ' + str(round(ma50,2) if ma50 else 'N/A'))
    print('100 day MA: ' + str(round(ma100,2) if ma100 else 'N/A'))
    print()
    print(determine_trend(latest_price, ma20, ma50, ma100))
