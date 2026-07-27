import sys
from spy_term_structure_alert import fetch_term_structure, build_email_body, build_commentary
from datetime import datetime

ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "SPY"

data = fetch_term_structure(ticker)
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(f"=== Term Structure Check - {ticker} ===")
print(f"UK time now: {now}")
print(f"ORATS tradeDate: {data.get('tradeDate')}")
print()
print(build_email_body(data))
print()
print(build_commentary(data))
