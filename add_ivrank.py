with open('spy_term_structure_alert.py', 'r') as f:
    content = f.read()

old_fetch = """    with urllib.request.urlopen(url2) as response:
        cores_data = json.loads(response.read())['data'][0]

    combined = {**summaries_data, **cores_data}
    return combined"""

new_fetch = """    with urllib.request.urlopen(url2) as response:
        cores_data = json.loads(response.read())['data'][0]

    ivrank_fields = 'ticker,tradeDate,ivRank1m,ivPct1m,ivRank1y,ivPct1y'
    url3 = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={TICKER}&fields={ivrank_fields}'
    with urllib.request.urlopen(url3) as response:
        ivrank_data = json.loads(response.read())['data'][0]

    combined = {**summaries_data, **cores_data, **ivrank_data}
    return combined"""

if old_fetch not in content:
    print("ERROR: fetch block not found, no changes made")
else:
    content = content.replace(old_fetch, new_fetch)
    with open('spy_term_structure_alert.py', 'w') as f:
        f.write(content)
    print("IV Rank fetch added successfully")
