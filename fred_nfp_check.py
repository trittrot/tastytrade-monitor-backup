"""
fred_nfp_check.py - Polls FRED for the latest US Non-Farm Payrolls print and
sends an SMS the moment a NEW release appears. Designed to run unattended via
cron on release-day mornings.

Series used: PAYEMS - "All Employees, Total Nonfarm", seasonally adjusted,
level in thousands of persons, released monthly (first Friday of the month,
8:30am ET).

Behaviour:
- If today is not the first Friday of the month, exits immediately (unless
  --force is passed).
- Otherwise polls FRED every POLL_INTERVAL_SECONDS, checking whether the
  latest observation date is newer than the last one we alerted on.
- Sends SMS the moment a new release appears, then exits.
- Gives up after MAX_WAIT_MINUTES and sends a "timed out" SMS if nothing new
  showed up (so a real problem doesn't go silent).
- Tracks last-alerted release date in a local state file, so re-running
  never double-texts for the same release.

Run manually (bypasses the day check): python3 fred_nfp_check.py --force
Run manually (respects the day check):  python3 fred_nfp_check.py
"""

import sys
import json
import time
from datetime import date, datetime

import requests
from secrets_loader import get_secret
from alerts import send_alert

FRED_SERIES_ID = "PAYEMS"
FRED_URL = "https://api.stlouisfed.org/fred/series/observations"
STATE_FILE = "fred_nfp_state.json"

POLL_INTERVAL_SECONDS = 60
MAX_WAIT_MINUTES = 75  # spans both EDT and EST possible release times


def is_first_friday(today: date) -> bool:
    return today.weekday() == 4 and today.day <= 7  # Friday == 4


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_alerted_release_date": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


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


def format_message(nfp):
    change = nfp["change_thousands"]
    sign = "+" if change >= 0 else ""
    return (
        f"US Non-Farm Payrolls (FRED PAYEMS)\n"
        f"Release date: {nfp['release_date']}\n"
        f"Change: {sign}{change:,.0f}k jobs\n"
        f"Total employment level: {nfp['level_thousands']:,.0f}k"
    )


def main():
    force = "--force" in sys.argv
    today = date.today()

    if not force and not is_first_friday(today):
        print(f"{today} is not NFP release day (first Friday). Exiting.")
        return

    state = load_state()
    last_alerted = state.get("last_alerted_release_date")

    deadline = time.time() + (MAX_WAIT_MINUTES * 60)
    attempt = 0

    while time.time() < deadline:
        attempt += 1
        try:
            nfp = get_latest_nfp()
        except Exception as e:
            print(f"[attempt {attempt}] FRED request failed: {e}")
            time.sleep(POLL_INTERVAL_SECONDS)
            continue

        if nfp["release_date"] != last_alerted:
            message = format_message(nfp)
            print(message)
            send_alert(message)
            state["last_alerted_release_date"] = nfp["release_date"]
            save_state(state)
            return

        print(
            f"[attempt {attempt}] No new release yet "
            f"(latest on file: {nfp['release_date']}). "
            f"Retrying in {POLL_INTERVAL_SECONDS}s."
        )
        time.sleep(POLL_INTERVAL_SECONDS)

    timeout_message = (
        f"FRED NFP check: gave up after {MAX_WAIT_MINUTES} min with no new "
        f"release detected (last known: {last_alerted}). Worth checking manually."
    )
    print(timeout_message)
    send_alert(timeout_message)


if __name__ == "__main__":
    main()
