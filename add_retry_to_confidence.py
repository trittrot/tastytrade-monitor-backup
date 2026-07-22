with open('etf_confidence_scan.py', 'r') as f:
    content = f.read()

old_block = """        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            for item in data['data']:
                results[item['ticker']] = item['confidence']"""

new_block = """        data = fetch_json_with_retry(url)
        for item in data['data']:
            results[item['ticker']] = item['confidence']"""

if old_block not in content:
    print("ERROR: block not found, no changes made")
else:
    content = content.replace(old_block, new_block)
    content = content.replace(
        "from secrets_loader import get_secret",
        "from secrets_loader import get_secret\nfrom orats_api_helper import fetch_json_with_retry"
    )
    with open('etf_confidence_scan.py', 'w') as f:
        f.write(content)
    print("Retry logic added to confidence scan")
