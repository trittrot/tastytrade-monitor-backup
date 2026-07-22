import urllib.request
import json
import csv
import os
import time
import smtplib
from email.mime.text import MIMEText
from datetime import date, datetime
from secrets_loader import get_secret
from alerts import send_alert
from etf_confidence_scan import is_cash_market_hours, QUALIFYING_PATH

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'etf_iv_percentile_log.csv')
IV_THRESHOLD = 80.0
POLL_INTERVAL_SECONDS = 300
alerted_today = set()
current_day = date.today().isoformat()

def get_qualifying_symbols():
    if not os.path.exists(QUALIFYING_PATH):
        return []
    with open(QUALIFYING_PATH, 'r') as f:
        reader = csv.DictReader(f)
        return [row['symbol'] for row in reader]

def fetch_iv_data(symbols):
    if not symbols:
        return {}
    token = get_secret('orats-api-token')
    results = {}
    for i in range(0, len(symbols), 10):
        batch = symbols[i:i+10]
        ticker_str = ','.join(batch)

        url1 = f'https://api.orats.io/datav2/cores?token={token}&ticker={ticker_str}&fields=ticker,ivPctile1y'
        with urllib.request.urlopen(url1) as response:
            data1 = json.loads(response.read())
            pctile_map = {item['ticker']: item.get('ivPctile1y') for item in data1['data']}

        url2 = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={ticker_str}&fields=ticker,ivRank1y'
        with urllib.request.urlopen(url2) as response:
            data2 = json.loads(response.read())
            rank_map = {item['ticker']: item.get('ivRank1y') for item in data2['data']}

        for t in batch:
            results[t] = (pctile_map.get(t), rank_map.get(t))
    return results

def send_iv_email(alerts_list, today, now):
    lines = ['ETF IV Percentile Alert - ' + today + ' at ' + now + ' UK', '']
    for symbol, pctile, rank in alerts_list:
        lines.append(symbol + ': IV Percentile ' + str(round(pctile,1)) + '% (threshold 80%), IV Rank ' + str(round(rank,1)) + '%')
    body = chr(10).join(lines)

    password = get_secret('miket-gmail-app-password').replace(' ', '')
    from_addr = get_secret('miket-email')
    to_addr = get_secret('mike-email')
    msg = MIMEText(body)
    msg['Subject'] = 'ETF IV Percentile Alert - ' + today
    msg['From'] = from_addr
    msg['To'] = to_addr
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())

def run_monitor():
    global current_day, alerted_today
    print('ETF IV Percentile checker started - reads qualifying list from confidence scan, ' + str(POLL_INTERVAL_SECONDS) + 's interval')
    while True:
        try:
            today = date.today().isoformat()
            now = datetime.now().strftime('%H:%M')

            if today != current_day:
                current_day = today
                alerted_today = set()
                print('New day: ' + today + ' - alert flags reset')

            if is_cash_market_hours():
                symbols = get_qualifying_symbols()
                iv_data = fetch_iv_data(symbols)

                file_exists = os.path.exists(LOG_PATH)
                with open(LOG_PATH, 'a', newline='') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(['date','time','symbol','iv_percentile','iv_rank','alerted'])
                    new_alerts = []
                    for symbol, (pctile, rank) in iv_data.items():
                        if pctile is None:
                            continue
                        triggered = pctile > IV_THRESHOLD
                        writer.writerow([today, now, symbol, pctile, rank, triggered])
                        if triggered and symbol not in alerted_today:
                            new_alerts.append((symbol, pctile, rank))
                            alerted_today.add(symbol)
                        elif not triggered and symbol in alerted_today:
                            alerted_today.discard(symbol)

                    if new_alerts:
                        symbol_list = ', '.join([a[0] for a in new_alerts])
                        sms_msg = 'Tastytrade ALERT: ETF IV Percentile above 80% - ' + symbol_list + '. Check email for details.'
                        send_alert(sms_msg)
                        send_iv_email(new_alerts, today, now)
                        print('[' + now + '] ALERT sent for: ' + symbol_list)
                    else:
                        print('[' + now + '] Checked ' + str(len(iv_data)) + ' qualifying symbols, no new alerts')
            else:
                print('[' + now + '] Outside cash market hours - skipping check')

        except Exception as e:
            print('Check error: ' + str(e))
            send_alert('Tastytrade monitor: ETF IV percentile check FAILED - ' + str(e))

        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == '__main__':
    run_monitor()
