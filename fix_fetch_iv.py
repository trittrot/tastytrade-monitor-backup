with open('etf_iv_percentile_alert.py', 'r') as f:
    content = f.read()

old_block = """def fetch_iv_data(symbols):
    if not symbols:
        return {}
    token = get_secret('orats-api-token')
    results = {}
    for i in range(0, len(symbols), 10):
        batch = symbols[i:i+10]
        ticker_str = ','.join(batch)
        url = f'https://api.orats.io/datav2/cores?token={token}&ticker={ticker_str}&fields=ticker,ivPctile1y,ivRank1y'
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            for item in data['data']:
                results[item['ticker']] = (item.get('ivPctile1y'), item.get('ivRank1y'))
    return results"""

new_block = """def fetch_iv_data(symbols):
    if not symbols:
        return {}
    token = get_secret('orats-api-token')
    results = {}
    for i in range(0, len(symbols), 10):
        batch = symbols[i:i+10]
        ticker_str = ','.join(batch)

        url1 = f'https://api.orats.io/datav2/cores?token={token}&ticker={ticker_str}&fields=ticker,ivPctile1y'
        with urllib.request.urlopen(url1) as response:
            data1 = json.loads(response.read())
            pctile_map = {item['ticker']: item.get('ivPctile1y') for item in data1['data']}

        url2 = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={ticker_str}&fields=ticker,ivRank1y'
        with urllib.request.urlopen(url2) as response:
            data2 = json.loads(response.read())
            rank_map = {item['ticker']: item.get('ivRank1y') for item in data2['data']}

        for t in batch:
            results[t] = (pctile_map.get(t), rank_map.get(t))
    return results"""

if old_block not in content:
    print("ERROR: block not found, no changes made")
else:
    content = content.replace(old_block, new_block)
    with open('etf_iv_percentile_alert.py', 'w') as f:
        f.write(content)
    print("Fetch function fixed - now correctly queries both Cores and IV Rank endpoints")
