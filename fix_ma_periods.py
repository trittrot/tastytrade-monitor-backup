with open('check_ma_trend.py', 'r') as f:
    content = f.read()

old_block = """    ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
    ma50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else None
    ma200 = sum(closes[-200:]) / 200 if len(closes) >= 200 else None

    return latest_date, latest_price, ma20, ma50, ma200"""

new_block = """    ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
    ma50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else None
    ma100 = sum(closes[-100:]) / 100 if len(closes) >= 100 else None

    return latest_date, latest_price, ma20, ma50, ma100"""

content = content.replace(old_block, new_block)

old_determine = """def determine_trend(price, ma20, ma50, ma200):
    if None in (ma20, ma50, ma200):
        return 'INSUFFICIENT DATA - not enough history for 200 day average'
    if price > ma20 and price > ma50 and price > ma200:
        return 'BULLISH - price above 20d, 50d, and 200d moving averages'
    elif price < ma20 and price < ma50 and price < ma200:
        return 'BEARISH - price below 20d, 50d, and 200d moving averages'
    else:
        return 'NEUTRAL - price mixed relative to moving averages, no clear trend alignment'"""

new_determine = """def determine_trend(price, ma20, ma50, ma100):
    if None in (ma20, ma50, ma100):
        return 'INSUFFICIENT DATA - not enough history for 100 day average'
    if price > ma20 and price > ma50 and price > ma100:
        return 'BULLISH - price above 20d, 50d, and 100d moving averages'
    elif price < ma20 and price < ma50 and price < ma100:
        return 'BEARISH - price below 20d, 50d, and 100d moving averages'
    else:
        return 'NEUTRAL - price mixed relative to moving averages, no clear trend alignment'"""

content = content.replace(old_determine, new_determine)

old_main = """    latest_date, latest_price, ma20, ma50, ma200 = calculate_moving_averages(prices)

    print()
    print('=== SPY Trend Determination - ' + latest_date + ' ===')
    print('Latest close: ' + str(latest_price))
    print('20 day MA: ' + str(round(ma20,2) if ma20 else 'N/A'))
    print('50 day MA: ' + str(round(ma50,2) if ma50 else 'N/A'))
    print('200 day MA: ' + str(round(ma200,2) if ma200 else 'N/A'))
    print()
    print(determine_trend(latest_price, ma20, ma50, ma200))"""

new_main = """    latest_date, latest_price, ma20, ma50, ma100 = calculate_moving_averages(prices)

    print()
    print('=== SPY Trend Determination - ' + latest_date + ' ===')
    print('Latest close: ' + str(latest_price))
    print('20 day MA: ' + str(round(ma20,2) if ma20 else 'N/A'))
    print('50 day MA: ' + str(round(ma50,2) if ma50 else 'N/A'))
    print('100 day MA: ' + str(round(ma100,2) if ma100 else 'N/A'))
    print()
    print(determine_trend(latest_price, ma20, ma50, ma100))"""

content = content.replace(old_main, new_main)

with open('check_ma_trend.py', 'w') as f:
    f.write(content)
print("Changed to 20d/50d/100d moving averages")
