import urllib.request
import json
import time
import smtplib
from email.mime.text import MIMEText
from datetime import date
from secrets_loader import get_secret
from alerts import send_alert

SYMBOLS = ['DIA','EEM','EWW','EWZ','FXI','GDX','GDXJ','GLD','IWM','QQQ','SLV','SMH','SPY','TLT','TQQQ','USO','UVXY','VXX','XLE','XLU','XOP']

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
            print(f'Confidence batch failed for {ticker_str}: {e}')
        time.sleep(0.2)
    return results

def fetch_iv_pct_batch(symbols, token):
    if not symbols:
        return {}
    results = {}
    for i in range(0, len(symbols), 10):
        batch = symbols[i:i+10]
        ticker_str = ','.join(batch)
        url = f'https://api.orats.io/datav2/ivrank?token={token}&ticker={ticker_str}&fields=ticker,ivPct1y'
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                for item in data['data']:
                    results[item['ticker']] = item.get('ivPct1y')
        except Exception as e:
            print(f'IV percentile batch failed for {ticker_str}: {e}')
        time.sleep(0.2)
    return results

def build_email_body(confidence_results, iv_results, today):
    conf_80 = set(t for t, c in confidence_results.items() if c > 0.80)

    stage2_80 = [t for t in conf_80 if iv_results.get(t) is not None and iv_results[t] > 80]
    stage2_90 = [t for t in conf_80 if iv_results.get(t) is not None and iv_results[t] > 90]

    stage2_80_sorted = sorted(stage2_80, key=lambda x: iv_results[x], reverse=True)
    stage2_90_sorted = sorted(stage2_90, key=lambda x: iv_results[x], reverse=True)

    lines = []
    lines.append('21 Liquid ETFs Two Stage Scan - ' + today)
    lines.append('Stage 1: ORATS confidence filter (above 80 percent). Stage 2: ivPct1y filter, applied only to Stage 1 qualifiers.')
    lines.append('')
    lines.append('Total ETFs scanned: ' + str(len(confidence_results)))
    lines.append('Stage 1 - confidence above 80 percent: ' + str(len(conf_80)) + ' symbols')
    lines.append('')
    lines.append('Stage 2 - also ivPct1y above 90 percent: ' + str(len(stage2_90_sorted)) + ' symbols')
    for t in stage2_90_sorted:
        lines.append('  ' + t + ': confidence ' + str(round(confidence_results[t]*100,2)) + '%, ivPct1y ' + str(round(iv_results[t],2)) + '%')
    lines.append('')
    lines.append('Stage 2 - also ivPct1y above 80 percent: ' + str(len(stage2_80_sorted)) + ' symbols')
    for t in stage2_80_sorted:
        lines.append('  ' + t + ': confidence ' + str(round(confidence_results[t]*100,2)) + '%, ivPct1y ' + str(round(iv_results[t],2)) + '%')

    return chr(10).join(lines)

def send_scan_email(body, today):
    password = get_secret('miket-gmail-app-password').replace(' ', '')
    from_addr = get_secret('miket-email')
    to_addr = get_secret('mike-email')

    msg = MIMEText(body)
    msg['Subject'] = 'ETF Two Stage Scan - ' + today
    msg['From'] = from_addr
    msg['To'] = to_addr

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())

def run_scan():
    try:
        token = get_secret('orats-api-token')
        today = date.today().isoformat()

        print('Stage 1: scanning ' + str(len(SYMBOLS)) + ' ETFs for confidence...')
        confidence_results = fetch_confidence_batch(SYMBOLS, token)

        conf_80_symbols = [t for t, c in confidence_results.items() if c > 0.80]
        print('Stage 1 complete: ' + str(len(conf_80_symbols)) + ' symbols above 80 percent confidence')

        print('Stage 2: checking ivPct1y for Stage 1 qualifiers...')
        iv_results = fetch_iv_pct_batch(conf_80_symbols, token)

        sms_msg = 'Tastytrade: ETF two stage scan complete. Check email for full details.'
        send_alert(sms_msg)

        body = build_email_body(confidence_results, iv_results, today)
        send_scan_email(body, today)
        print('Scan complete - SMS and email sent')

    except Exception as e:
        send_alert('Tastytrade monitor: ETF two stage scan FAILED - ' + str(e))
        raise

if __name__ == '__main__':
    run_scan()
