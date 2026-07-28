with open('etf_iv_percentile_alert.py', 'r') as f:
    content = f.read()

old_import = "from etf_confidence_scan import is_cash_market_hours, QUALIFYING_PATH"
new_import = """from etf_confidence_scan import QUALIFYING_PATH
from datetime import datetime as dt_check

CASH_MARKET_OPEN_HOUR = 14
CASH_MARKET_OPEN_MINUTE = 40
CASH_MARKET_CLOSE_HOUR = 21
CASH_MARKET_CLOSE_MINUTE = 0

def is_cash_market_hours():
    now = dt_check.now()
    if now.weekday() >= 5:
        return False
    open_time = now.replace(hour=CASH_MARKET_OPEN_HOUR, minute=CASH_MARKET_OPEN_MINUTE, second=0, microsecond=0)
    close_time = now.replace(hour=CASH_MARKET_CLOSE_HOUR, minute=CASH_MARKET_CLOSE_MINUTE, second=0, microsecond=0)
    return open_time <= now <= close_time"""

if old_import not in content:
    print("ERROR: import line not found")
else:
    content = content.replace(old_import, new_import)
    with open('etf_iv_percentile_alert.py', 'w') as f:
        f.write(content)
    print("Stage 2 now has its own independent market-hours check, starting 14:40")
