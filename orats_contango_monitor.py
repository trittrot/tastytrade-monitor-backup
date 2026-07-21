import urllib.request
import json
import csv
import os
import smtplib
from email.mime.text import MIMEText
from datetime import date
from secrets_loader import get_secret
from alerts import send_alert

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orats_contango_log.csv')
TICKER = 'SPY'
WINDOW_DAYS = 15
MA_DAYS = 10
CAUTION_THRESHOLD = 0.88
SIGNIFICANT_THRESHOLD = 2.0

def fetch_contango():
    token = get_secret('orats-api-token')
    url = f'https://api.orats.io/datav2/cores?token={token}&ticker={TICKER}&fields=tradeDate,contango'
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data['data'][0]['contango'], data['data'][0]['tradeDate']

def get_previous_reading(log_path, today):
    if not os.path.exists(log_path):
        return None
    with open(log_path, 'r') as f:
        rows = list(csv.reader(f))
    for row in reversed(rows[1:]):
        if row[0] != today:
            return float(row[1])
    return None

def get_moving_average(log_path, n, today):
    if not os.path.exists(log_path):
        return None
    with open(log_path, 'r') as f:
        rows = list(csv.reader(f))
    data_rows = [r for r in rows[1:] if r[0] != today]
    if len(data_rows) < n:
        return None
    last_n = data_rows[-n:]
    values = [float(r[1]) for r in last_n]
    return sum(values) / len(values)

def get_label(deviation_pts):
    abs_dev = abs(deviation_pts)
    if abs_dev >= SIGNIFICANT_THRESHOLD:
        return 'SIGNIFICANT'
    elif abs_dev >= CAUTION_THRESHOLD:
        return 'CAUTION'
    else:
        return 'ROUTINE'

def get_rolling_window(log_path, n):
    if not os.path.exists(log_path):
        return []
    with open(log_path, 'r') as f:
        rows = list(csv.reader(f))
    data_rows = rows[1:]
    return data_rows[-n:]

def send_report_email(window_rows, today_ma, today_val, today_deviation_pts):
    lines = []
    for i in range(1, len(window_rows)):
        prev_date, prev_val = window_rows[i-1][0], float(window_rows[i-1][1])
        curr_date, curr_val = window_rows[i][0], float(window_rows[i][1])
        if prev_val != 0:
            pct = (curr_val - prev_val) / abs(prev_val) * 100
        else:
            pct = float('inf')
        lines.append(prev_date + ' -> ' + curr_date + ': ' + format(prev_val, '+.4f') + ' -> ' + format(curr_val, '+.4f') + '  change ' + format(pct, '+.1f') + ' percent')

    ma_section = 'No 10 day moving average yet, not enough history'
    if today_ma is not None:
        label = get_label(today_deviation_pts)
        ma_section = '10 day moving average: ' + format(today_ma, '+.4f') + '. Todays value: ' + format(today_val, '+.4f') + '. Deviation: ' + format(today_deviation_pts, '+.3f') + ' points (' + label + ')'

    body = 'ORATS SPY Contango - Rolling 15 Trading Day Report' + chr(10) + chr(10) + ma_section + chr(10) + chr(10) + chr(10).join(lines)

    password = get_secret('miket-gmail-app-password').replace(' ', '')
    from_addr = get_secret('miket-email')
    to_addr = get_secret('mike-email')

    msg = MIMEText(body)
    msg['Subject'] = 'Tastytrade Monitor - Contango Report ' + date.today().isoformat()
    msg['From'] = from_addr
    msg['To'] = to_addr

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())

def run_check():
    contango, trade_date = fetch_contango()
    today = date.today().isoformat()

    print('ORATS contango for ' + trade_date + ': ' + str(contango))

    prev = get_previous_reading(LOG_PATH, today)
    ma = get_moving_average(LOG_PATH, MA_DAYS, today)

    deviation_pts = None
    label = None
    if ma is not None:
        deviation_pts = contango - ma
        label = get_label(deviation_pts)
        print('10 day moving average: ' + str(round(ma,4)) + '  Deviation: ' + str(round(deviation_pts,3)) + ' points (' + label + ')')

    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'contango', 'pct_change'])

        pct_change = None
        if prev is not None and prev != 0:
            pct_change = (contango - prev) / abs(prev) * 100
            print('Previous reading: ' + str(prev) + '  Change: ' + str(round(pct_change,1)) + '%')
            sms_msg = 'Tastytrade: ORATS contango SPY = ' + str(round(contango,3)) + ' (' + str(round(pct_change,1)) + '% vs prev day)'
        else:
            print('No previous reading to compare against yet')
            sms_msg = 'Tastytrade: ORATS contango SPY = ' + str(round(contango,3)) + ' (no prior day to compare)'

        if deviation_pts is not None:
            sms_msg = sms_msg + '. 10MA dev: ' + str(round(deviation_pts,3)) + 'pts (' + label + ')'
            if label == 'CAUTION':
                sms_msg = sms_msg + '. Monitor closely.'
            elif label == 'SIGNIFICANT':
                sms_msg = sms_msg + '. Per your plan: consider closing short legs, hold/increase long put hedge.'

        sms_msg = sms_msg + '. Check email for 3wk report.'

        writer.writerow([today, contango, round(pct_change, 2) if pct_change is not None else ''])

    send_alert(sms_msg)

    window_rows = get_rolling_window(LOG_PATH, WINDOW_DAYS)
    if len(window_rows) >= 2:
        send_report_email(window_rows, ma, contango, deviation_pts)
        print('Report email sent')
    else:
        print('Not enough history yet for report email')

    return contango

if __name__ == '__main__':
    try:
        run_check()
    except Exception as e:
        send_alert('Tastytrade monitor: ORATS contango check FAILED - ' + str(e))
        raise
