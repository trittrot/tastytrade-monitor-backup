with open('check_ma_trend.py', 'r') as f:
    content = f.read()

old_block = """    prices = []
    current = start
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
            except Exception:
                pass
        current += timedelta(days=1)
    return prices"""

new_block = """    prices = []
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
            except Exception:
                pass
            count += 1
            if count % 50 == 0:
                print('Fetched ' + str(count) + ' days so far, at ' + date_str)
        current += timedelta(days=1)
    return prices"""

if old_block not in content:
    print("ERROR: block not found")
else:
    content = content.replace(old_block, new_block)
    with open('check_ma_trend.py', 'w') as f:
        f.write(content)
    print("Progress printing added")
