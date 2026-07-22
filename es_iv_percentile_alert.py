import json
import csv
import os
import smtplib
from email.mime.text import MIMEText
from datetime import date, datetime
from auth import authenticate_production
from alerts import send_alert
from secrets_loader import get_secret

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'es_iv_percentile_log.csv')
THRESHOLD = 80.0

def fetch_es_iv_metrics():
    session = authenticate_production()
    data = session._get('/market-metrics?symbols=/ES')
    metrics = data['items'][0]
    iv_pctile = float(metrics['implied-volatility-percentile']) * 100
    iv_rank = float(metrics['implied-volatility-index-rank']) * 100
    return iv_pctile, iv_rank

def run_check():
    try:
        iv_pctile, iv_rank = fetch_es_iv_metrics()
        today = date.today().isoformat()
        now = datetime.now().strftime('%H:%M')

        print('ES IV Percentile: ' + str(round(iv_pctile,1)) + '%  IV Rank: ' + str(round(iv_rank,1)) + '%')

        file_exists = os.path.exists(LOG_PATH)
        with open(LOG_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['date', 'time', 'iv_percentile', 'iv_rank', 'alerted'])
            alerted = iv_pctile > THRESHOLD
            writer.writerow([today, now, round(iv_pctile,2), round(iv_rank,2), alerted])

        if iv_pctile > THRESHOLD:
            sms_msg = 'Tastytrade ALERT: ES IV Percentile ' + str(round(iv_pctile,1)) + '% exceeds ' + str(THRESHOLD) + '% threshold. IV Rank: ' + str(round(iv_rank,1)) + '%'
            send_alert(sms_msg)

            email_body = 'ES IV Percentile Alert - ' + today + ' at ' + now + ' UK' + chr(10) + chr(10)
            email_body = email_body + 'IV Percentile: ' + str(round(iv_pctile,2)) + '% (threshold: ' + str(THRESHOLD) + '%)' + chr(10)
            email_body = email_body + 'IV Rank: ' + str(round(iv_rank,2)) + '%' + chr(10)

            password = get_secret('miket-gmail-app-password').replace(' ', '')
            from_addr = get_secret('miket-email')
            to_addr = get_secret('mike-email')
            msg = MIMEText(email_body)
            msg['Subject'] = 'ES IV Percentile Alert - ' + today
            msg['From'] = from_addr
            msg['To'] = to_addr
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(from_addr, password)
                server.sendmail(from_addr, [to_addr], msg.as_string())

            print('Alert sent - IV percentile above threshold')
        else:
            print('No alert - IV percentile below threshold')

        return iv_pctile
    except Exception as e:
        send_alert('Tastytrade monitor: ES IV percentile check FAILED - ' + str(e))
        raise

if __name__ == '__main__':
    run_check()
