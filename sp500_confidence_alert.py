import urllib.request
import json
import time
import smtplib
from email.mime.text import MIMEText
from datetime import date, datetime
from secrets_loader import get_secret
from alerts import send_alert

def load_symbols():
    with open('sp500_symbols.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def fetch_confidence_batch(symbols, token):
    results = {}
    for i in range(0, len(symbols), 10):
        batch = symbols[i:i+10]
        ticker_str = ','.join(batch)
        url = f'https://api.orats.io/datav2/summaries?token={token}&ticker={ticker_str}&fields=ticker,confidence'
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                for item in data['data']:
                    results[item['ticker']] = item['confidence']
        except Exception as e:
            print(f'Batch failed for {ticker_str}: {e}')
        time.sleep(0.2)
    return results

def build_email_body(results, today):
    above_80 = sorted([t for t, c in results.items() if c > 0.80], key=lambda x: results[x], reverse=True)
    above_90 = sorted([t for t, c in results.items() if c > 0.90], key=lambda x: results[x], reverse=True)

    lines = []
    lines.append('S&P 500 Confidence Scan - ' + today)
    lines.append('Total symbols scanned: ' + str(len(results)))
    lines.append('')
    lines.append('Above 90 percent confidence: ' + str(len(above_90)) + ' symbols')
    for t in above_90:
        lines.append('  ' + t + ': ' + str(round(results[t]*100, 2)) + '%')
    lines.append('')
    lines.append('Above 80 percent confidence (includes above 90 list): ' + str(len(above_80)) + ' symbols')
    for t in above_80:
        if t not in above_90:
            lines.append('  ' + t + ': ' + str(round(results[t]*100, 2)) + '%')

    return chr(10).join(lines)

def send_confidence_email(body, today):
    password = get_secret('miket-gmail-app-password').replace(' ', '')
    from_addr = get_secret('miket-email')
    to_addr = get_secret('mike-email')

    msg = MIMEText(body)
    msg['Subject'] = 'S&P 500 Confidence Scan - ' + today
    msg['From'] = from_addr
    msg['To'] = to_addr

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())

def run_scan():
    try:
        token = get_secret('orats-api-token')
        symbols = load_symbols()
        today = date.today().isoformat()

        print('Scanning ' + str(len(symbols)) + ' S&P 500 symbols...')
        results = fetch_confidence_batch(symbols, token)

        above_80 = [t for t, c in results.items() if c > 0.80]
        above_90 = [t for t, c in results.items() if c > 0.90]

        print('Above 80%: ' + str(len(above_80)) + '  Above 90%: ' + str(len(above_90)))

        sms_msg = 'Tastytrade: S&P 500 Confidence Scan - ' + str(len(above_80)) + ' above 80%, ' + str(len(above_90)) + ' above 90%. Check email for full list.'
        send_alert(sms_msg)

        body = build_email_body(results, today)
        send_confidence_email(body, today)
        print('Scan complete - SMS and email sent')

    except Exception as e:
        send_alert('Tastytrade monitor: S&P 500 confidence scan FAILED - ' + str(e))
        raise

if __name__ == '__main__':
    run_scan()
