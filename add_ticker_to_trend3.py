with open('check_ma_trend.py', 'r') as f:
    lines = f.readlines()

split_index = None
for i, line in enumerate(lines):
    if line.strip().startswith("if __name__"):
        split_index = i
        break

if split_index is None:
    print("ERROR: could not find if __name__ line")
else:
    kept_lines = lines[:split_index]

    new_block = """if __name__ == '__main__':
    import sys
    ticker = sys.argv[1].upper() if len(sys.argv) > 1 else 'SPY'
    print('Fetching ' + ticker + ' daily price history, this will take a few minutes...')
    prices = fetch_daily_prices(ticker, 420)
    print('Total trading days fetched: ' + str(len(prices)))
    latest_date, latest_price, ma20, ma50, ma100 = calculate_moving_averages(prices)
    print()
    print('=== ' + ticker + ' Trend Determination - ' + latest_date + ' ===')
    print('Latest close: ' + str(latest_price))
    print('20 day MA: ' + str(round(ma20,2) if ma20 else 'N/A'))
    print('50 day MA: ' + str(round(ma50,2) if ma50 else 'N/A'))
    print('100 day MA: ' + str(round(ma100,2) if ma100 else 'N/A'))
    print()
    print(determine_trend(latest_price, ma20, ma50, ma100))
"""

    with open('check_ma_trend.py', 'w') as f:
        f.writelines(kept_lines)
        f.write(new_block)

    print("Successfully replaced main block - trend now accepts optional ticker argument")
