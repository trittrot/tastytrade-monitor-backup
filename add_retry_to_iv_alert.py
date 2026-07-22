with open('etf_iv_percentile_alert.py', 'r') as f:
    content = f.read()

old_block = """        url1 = f'https://api.orats.io/datav2/cores?token={token}&ticker={ticker_str}&fields=ticker,ivPctile1y'
        with urllib.request.urlopen(url1) as response:
            data1 = json.loads(response.read())
            pctile_map = {item['ticker']: item.get('ivPctile1y') for item in data1['data']}

        url2 = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={ticker_str}&fields=ticker,ivRank1y'
        with urllib.request.urlopen(url2) as response:
            data2 = json.loads(response.read())
            rank_map = {item['ticker']: item.get('ivRank1y') for item in data2['data']}"""

new_block = """        url1 = f'https://api.orats.io/datav2/cores?token={token}&ticker={ticker_str}&fields=ticker,ivPctile1y'
        data1 = fetch_json_with_retry(url1)
        pctile_map = {item['ticker']: item.get('ivPctile1y') for item in data1['data']}

        url2 = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={ticker_str}&fields=ticker,ivRank1y'
        data2 = fetch_json_with_retry(url2)
        rank_map = {item['ticker']: item.get('ivRank1y') for item in data2['data']}"""

if old_block not in content:
    print("ERROR: block not found, no changes made")
else:
    content = content.replace(old_block, new_block)
    content = content.replace(
        "from secrets_loader import get_secret",
        "from secrets_loader import get_secret\nfrom orats_api_helper import fetch_json_with_retry"
    )
    with open('etf_iv_percentile_alert.py', 'w') as f:
        f.write(content)
    print("Retry logic added to IV percentile alert")
