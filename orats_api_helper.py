import urllib.request
import json
import time

def fetch_json_with_retry(url, max_retries=3, delay_seconds=5):
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read())
        except Exception as e:
            last_error = e
            print(f"Attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                time.sleep(delay_seconds)
    raise last_error
