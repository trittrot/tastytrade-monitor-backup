with open('spy_term_structure_alert.py', 'r') as f:
    content = f.read()

old_line = "def fetch_term_structure():"
new_line = "def fetch_term_structure(ticker=None):\n    if ticker is None:\n        ticker = TICKER"

if old_line not in content:
    print("ERROR: line not found")
else:
    content = content.replace(old_line, new_line, 1)
    with open('spy_term_structure_alert.py', 'w') as f:
        f.write(content)
    print("fetch_term_structure now accepts optional ticker parameter")
