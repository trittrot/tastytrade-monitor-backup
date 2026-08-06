"""
fred_nfp_check.py - Fetches the latest US Non-Farm Payrolls print from the
St Louis Fed (FRED) API and sends an SMS alert.

Series used: PAYEMS - "All Employees, Total Nonfarm", seasonally adjusted,
level in thousands of persons, released monthly (usually first Friday).

This is an on-demand test script, not yet on the cron schedule.
Run manually: python3 fred_nfp_check.py
"""

import requests
from datetime import datetime
from secrets_loader import get_secret
from alerts import send_alert

FRED_SERIES_ID = "PAYEMS"
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"


def get_latest_nfp():
    api_key = get_secret("fred-api-key")
    params = {
        "series_id": FRED_SERIES_ID,
        "api_key": api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 2,
    }
    response = requests.get(FRED_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    observations = data.get("observations", [])
    if len(observations) < 2:
        raise ValueError(f"Expected 2 observations, got {len(observations)}")

    latest, previous = observations[0], observations[1]
    latest_value = float(latest["value"])
    previous_value = float(previous["value"])
    change_thousands = latest_value - previous_value

    return {
        "release_date": latest["date"],
        "level_thousands": latest_value,
        "change_thousands": change_thousands,
    }


def main():
    try:
        nfp = get_latest_nfp()
        change = nfp["change_thousands"]
        sign = "+" if change >= 0 else ""
        message = (
            f"US Non-Farm Payrolls (FRED PAYEMS)\n"
            f"Release date on file: {nfp['release_date']}\n"
            f"Change: {sign}{change:,.0f}k jobs\n"
            f"Total employment level: {nfp['level_thousands']:,.0f}k"
        )
        print(message)
        send_alert(message)
    except Exception as e:
        error_message = f"FRED NFP check FAILED: {e}"
        print(error_message)
        send_alert(error_message)


if __name__ == "__main__":
    main()
