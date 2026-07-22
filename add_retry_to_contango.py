with open('orats_contango_monitor.py', 'r') as f:
    content = f.read()

old_block = """    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data['data'][0]['contango'], data['data'][0]['tradeDate']"""

new_block = """    data = fetch_json_with_retry(url)
    return data['data'][0]['contango'], data['data'][0]['tradeDate']"""

if old_block not in content:
    print("ERROR: block not found, no changes made")
else:
    content = content.replace(old_block, new_block)
    content = content.replace(
        "from secrets_loader import get_secret",
        "from secrets_loader import get_secret\nfrom orats_api_helper import fetch_json_with_retry"
    )
    with open('orats_contango_monitor.py', 'w') as f:
        f.write(content)
    print("Retry logic added to contango monitor")
