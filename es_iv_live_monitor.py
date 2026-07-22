import json
import csv
import os
import time
import smtplib
from email.mime.text import MIMEText
from datetime import date, datetime, timedelta
from auth import authenticate_production
from alerts import send_alert
from secrets_loader import get_secret

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'es_iv_percentile_log.csv')
THRESHOLD = 80.0
POLL_INTERVAL_SECONDS = 60
REAUTH_INTERVAL_HOURS = 4

def fetch_es_iv_metrics(session):
    data = session._get('/market-metrics?symbols=/ES')
    metrics = data['items'][0]
    iv_pctile = float(metrics['implied-volatility-percentile']) * 100
    iv_rank = float(metrics['implied-volatility-index-rank']) * 100
    return iv_pctile, iv_rank

def send_iv_email(iv_pctile, iv_rank, today, now):
    body = 'ES IV Percentile Alert - ' + today + ' at ' + now + ' UK' + chr(10) + chr(10)
    body = body + 'IV Percentile: ' + str(round(iv_pctile,2)) + '% (threshold: ' + str(THRESHOLD) + '%)' + chr(10)
    body = body + 'IV Rank: ' + str(round(iv_rank,2)) + '%' + chr(10)

    password = get_secret('miket-gmail-app-password').replace(' ', '')
    from_addr = get_secret('miket-email')
    to_addr = get_secret('mike-email')
    msg = MIMEText(body)
    msg['Subject'] = 'ES IV Percentile Alert - ' + today
    msg['From'] = from_addr
    msg['To'] = to_addr
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())

def run_monitor():
    while True:
        try:
            session = authenticate_production()
            session_start = datetime.now()
            today = date.today().isoformat()
            already_alerted = False

            print('[' + datetime.now().strftime('%H:%M:%S') + '] Authenticated. Starting ES IV percentile monitor for ' + today)

            while True:
                if datetime.now() - session_start > timedelta(hours=REAUTH_INTERVAL_HOURS):
                    print('[' + datetime.now().strftime('%H:%M:%S') + '] Scheduled re-authentication')
                    break

                current_today = date.today().isoformat()
                if current_today != today:
                    today = current_today
                    already_alerted = False
                    print('New day: ' + today + ' - alert flag reset')

                try:
                    iv_pctile, iv_rank = fetch_es_iv_metrics(session)
                    now = datetime.now().strftime('%H:%M')

                    file_exists = os.path.exists(LOG_PATH)
                    with open(LOG_PATH, 'a', newline='') as f:
                        writer = csv.writer(f)
                        if not file_exists:
                            writer.writerow(['date', 'time', 'iv_percentile', 'iv_rank', 'alerted'])
                        triggered_now = iv_pctile > THRESHOLD
                        writer.writerow([today, now, round(iv_pctile,2), round(iv_rank,2), triggered_now])

                    if iv_pctile > THRESHOLD and not already_alerted:
                        sms_msg = 'Tastytrade ALERT: ES IV Percentile ' + str(round(iv_pctile,1)) + '% exceeds ' + str(THRESHOLD) + '% threshold. IV Rank: ' + str(round(iv_rank,1)) + '%'
                        send_alert(sms_msg)
                        send_iv_email(iv_pctile, iv_rank, today, now)
                        already_alerted = True
                        print('[' + now + '] ALERT sent - IV percentile ' + str(round(iv_pctile,1)) + '%')
                    elif iv_pctile <= THRESHOLD and already_alerted:
                        already_alerted = False
                        print('[' + now + '] IV percentile back below threshold, alert flag reset')

                except Exception as e:
                    print('Poll error: ' + str(e))

                time.sleep(POLL_INTERVAL_SECONDS)

        except Exception as e:
            print('[' + datetime.now().strftime('%H:%M:%S') + '] Error: ' + str(e) + ' - reconnecting in 10s')
            time.sleep(10)

if __name__ == '__main__':
    run_monitor()
