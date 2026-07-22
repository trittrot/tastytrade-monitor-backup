import urllib.request
import json
import csv
import os
import time
from datetime import date, datetime, timedelta
from secrets_loader import get_secret
from orats_api_helper import fetch_json_with_retry
from alerts import send_alert

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etf_confidence_log.csv')
QUALIFYING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etf_qualifying_symbols.csv')
SYMBOLS = ['DIA','EEM','EWW','EWZ','FXI','GDX','GDXJ','GLD','IWM','QQQ','SLV','SMH','SPY','TLT','TQQQ','USO','UVXY','VXX','XLE','XLU','XOP']
CONFIDENCE_THRESHOLD = 0.90
POLL_INTERVAL_SECONDS = 300

CASH_MARKET_OPEN_HOUR = 14
CASH_MARKET_OPEN_MINUTE = 30
CASH_MARKET_CLOSE_HOUR = 21
CASH_MARKET_CLOSE_MINUTE = 0

def is_cash_market_hours():
    now = datetime.now()
    if now.weekday() >= 5:
        return False
    open_time = now.replace(hour=CASH_MARKET_OPEN_HOUR, minute=CASH_MARKET_OPEN_MINUTE, second=0, microsecond=0)
    close_time = now.replace(hour=CASH_MARKET_CLOSE_HOUR, minute=CASH_MARKET_CLOSE_MINUTE, second=0, microsecond=0)
    return open_time <= now <= close_time

def fetch_confidence_batch():
    token = get_secret('orats-api-token')
    results = {}
    for i in range(0, len(SYMBOLS), 10):
        batch = SYMBOLS[i:i+10]
        ticker_str = ','.join(batch)
        url = f'https://api.orats.io/datav2/summaries?token={token}&ticker={ticker_str}&fields=ticker,confidence'
        data = fetch_json_with_retry(url)
        for item in data['data']:
            results[item['ticker']] = item['confidence']
    return results

def write_qualifying_list(results):
    qualifying = [t for t, c in results.items() if c > CONFIDENCE_THRESHOLD]
    with open(QUALIFYING_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['symbol', 'confidence', 'updated_at'])
        now_str = datetime.now().isoformat(timespec='seconds')
        for t in qualifying:
            writer.writerow([t, round(results[t], 4), now_str])
    return qualifying

def log_scan(results, qualifying):
    today = date.today().isoformat()
    now = datetime.now().strftime('%H:%M')
    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'time', 'symbol', 'confidence', 'qualifies'])
        for ticker, conf in results.items():
            writer.writerow([today, now, ticker, round(conf, 4), conf > CONFIDENCE_THRESHOLD])
    print('[' + now + '] Scanned ' + str(len(results)) + ' symbols, ' + str(len(qualifying)) + ' qualify (confidence > ' + str(CONFIDENCE_THRESHOLD) + ')')

def run_monitor():
    print('ETF confidence scanner started - cash market hours only, ' + str(POLL_INTERVAL_SECONDS) + 's interval')
    while True:
        try:
            if is_cash_market_hours():
                results = fetch_confidence_batch()
                qualifying = write_qualifying_list(results)
                log_scan(results, qualifying)
            else:
                print('[' + datetime.now().strftime('%H:%M') + '] Outside cash market hours - skipping scan')
        except Exception as e:
            print('Scan error: ' + str(e))
            send_alert('Tastytrade monitor: ETF confidence scan FAILED - ' + str(e))

        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == '__main__':
    run_monitor()
