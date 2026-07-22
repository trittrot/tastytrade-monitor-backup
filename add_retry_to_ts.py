with open('spy_term_structure_alert.py', 'r') as f:
    content = f.read()

old_block = """    with urllib.request.urlopen(url1) as response:
        summaries_data = json.loads(response.read())['data'][0]

    with urllib.request.urlopen(url2) as response:
        cores_data = json.loads(response.read())['data'][0]

    ivrank_fields = 'ticker,tradeDate,ivRank1m,ivPct1m,ivRank1y,ivPct1y'
    url3 = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={TICKER}&fields={ivrank_fields}'
    with urllib.request.urlopen(url3) as response:
        ivrank_data = json.loads(response.read())['data'][0]"""

new_block = """    summaries_data = fetch_json_with_retry(url1)['data'][0]
    cores_data = fetch_json_with_retry(url2)['data'][0]

    ivrank_fields = 'ticker,tradeDate,ivRank1m,ivPct1m,ivRank1y,ivPct1y'
    url3 = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={TICKER}&fields={ivrank_fields}'
    ivrank_data = fetch_json_with_retry(url3)['data'][0]"""

if old_block not in content:
    print("ERROR: block not found, no changes made")
else:
    content = content.replace(old_block, new_block)
    content = content.replace(
        "from secrets_loader import get_secret",
        "from secrets_loader import get_secret\nfrom orats_api_helper import fetch_json_with_retry"
    )
    with open('spy_term_structure_alert.py', 'w') as f:
        f.write(content)
    print("Retry logic added successfully")
