import urllib.request
import json
import csv
import os
import smtplib
from email.mime.text import MIMEText
from datetime import date, datetime
from secrets_loader import get_secret
from alerts import send_alert

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spy_term_structure_log.csv')
TICKER = 'SPY'

SUMMARIES_FIELDS = 'ticker,tradeDate,exErnIv10d,exErnIv20d,exErnIv30d,exErnIv60d,exErnIv90d,exErnIv6m,exErnIv1y,contango,fwd30_20,fwd60_30,fwd90_60,fwd180_90,fwd90_30,fbfwd30_20,fbfwd60_30,fbfwd90_60,fbfwd180_90,fbfwd90_30,confidence,iv30d,rSlp30'
CORES_FIELDS = 'ticker,tradeDate,slope,slopeInf,slopeFcst,slopeFcstInf,slopepctile,ivPctile1y,ivHvXernRatio,orHvXern20d,deriv,derivInf'

def fetch_term_structure():
    token = get_secret('orats-api-token')
    url1 = f'https://api.orats.io/datav2/summaries?token={token}&ticker={TICKER}&fields={SUMMARIES_FIELDS}'
    url2 = f'https://api.orats.io/datav2/cores?token={token}&ticker={TICKER}&fields={CORES_FIELDS}'

    with urllib.request.urlopen(url1) as response:
        summaries_data = json.loads(response.read())['data'][0]

    with urllib.request.urlopen(url2) as response:
        cores_data = json.loads(response.read())['data'][0]

    combined = {**summaries_data, **cores_data}
    return combined

FIELD_ORDER = ['tradeDate','exErnIv10d','exErnIv20d','exErnIv30d','exErnIv60d','exErnIv90d','exErnIv6m','exErnIv1y','contango','fwd30_20','fwd60_30','fwd90_60','fwd180_90','fwd90_30','fbfwd30_20','fbfwd60_30','fbfwd90_60','fbfwd180_90','fbfwd90_30','confidence','iv30d','rSlp30','slope','slopeInf','slopeFcst','slopeFcstInf','slopepctile','ivPctile1y','ivHvXernRatio','orHvXern20d','deriv','derivInf']

def log_term_structure(data):
    today = date.today().isoformat()
    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(FIELD_ORDER)
        row = [data.get(field, '') for field in FIELD_ORDER]
        writer.writerow(row)

def build_email_body(data):
    lines = []
    lines.append('SPY Term Structure Snapshot - ' + data.get('tradeDate','') + ' at ' + datetime.now().strftime('%H:%M') + ' UK' + chr(10))
    lines.append('Confidence: ' + str(data.get('confidence','')))
    lines.append('')
    lines.append('Ex-earnings IV curve:')
    lines.append('  10d: ' + str(data.get('exErnIv10d','')))
    lines.append('  20d: ' + str(data.get('exErnIv20d','')))
    lines.append('  30d: ' + str(data.get('exErnIv30d','')))
    lines.append('  60d: ' + str(data.get('exErnIv60d','')))
    lines.append('  90d: ' + str(data.get('exErnIv90d','')))
    lines.append('  6m: ' + str(data.get('exErnIv6m','')))
    lines.append('  1y: ' + str(data.get('exErnIv1y','')))
    lines.append('')
    lines.append('Contango: ' + str(data.get('contango','')))
    lines.append('')
    lines.append('Forward curve:')
    lines.append('  fwd30_20: ' + str(data.get('fwd30_20','')))
    lines.append('  fwd60_30: ' + str(data.get('fwd60_30','')))
    lines.append('  fwd90_60: ' + str(data.get('fwd90_60','')))
    lines.append('  fwd180_90: ' + str(data.get('fwd180_90','')))
    lines.append('  fwd90_30: ' + str(data.get('fwd90_30','')))
    lines.append('')
    lines.append('Forward anomaly check (flat forward / forward ratio):')
    lines.append('  fbfwd30_20: ' + str(data.get('fbfwd30_20','')))
    lines.append('  fbfwd60_30: ' + str(data.get('fbfwd60_30','')))
    lines.append('  fbfwd90_60: ' + str(data.get('fbfwd90_60','')))
    lines.append('  fbfwd180_90: ' + str(data.get('fbfwd180_90','')))
    lines.append('  fbfwd90_30: ' + str(data.get('fbfwd90_30','')))
    lines.append('')
    lines.append('iv30d: ' + str(data.get('iv30d','')))
    lines.append('rSlp30: ' + str(data.get('rSlp30','')))
    lines.append('')
    lines.append('Slope family:')
    lines.append('  slope: ' + str(data.get('slope','')))
    lines.append('  slopeInf: ' + str(data.get('slopeInf','')))
    lines.append('  slopeFcst: ' + str(data.get('slopeFcst','')))
    lines.append('  slopeFcstInf: ' + str(data.get('slopeFcstInf','')))
    lines.append('  slopepctile: ' + str(data.get('slopepctile','')))
    lines.append('')
    lines.append('ivPctile1y: ' + str(data.get('ivPctile1y','')))
    lines.append('ivHvXernRatio: ' + str(data.get('ivHvXernRatio','')))
    lines.append('orHvXern20d: ' + str(data.get('orHvXern20d','')))
    lines.append('')
    lines.append('deriv: ' + str(data.get('deriv','')))
    lines.append('derivInf: ' + str(data.get('derivInf','')))
    return chr(10).join(lines)

def send_term_structure_email(body):
    password = get_secret('miket-gmail-app-password').replace(' ', '')
    from_addr = get_secret('miket-email')
    to_addr = get_secret('mike-email')

    msg = MIMEText(body)
    msg['Subject'] = 'SPY Term Structure - ' + date.today().isoformat()
    msg['From'] = from_addr
    msg['To'] = to_addr

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())

def run_check():
    try:
        data = fetch_term_structure()
        log_term_structure(data)
        body = build_email_body(data) + chr(10) + chr(10) + build_commentary(data)
        send_term_structure_email(body)
        send_alert('SPY term structure updated, please check email now for details')
        print('Term structure logged, emailed, and SMS sent successfully')
    except Exception as e:
        send_alert('Tastytrade monitor: SPY term structure check FAILED - ' + str(e))
        raise


def categorize(value, low_thresh=33, high_thresh=66):
    if value is None or value == '':
        return 'unknown'
    if value < low_thresh:
        return 'low'
    elif value > high_thresh:
        return 'high'
    else:
        return 'moderate'

def build_commentary(data):
    lines = []
    lines.append('--- Commentary ---')

    tenors = ['exErnIv10d','exErnIv20d','exErnIv30d','exErnIv60d','exErnIv90d','exErnIv6m','exErnIv1y']
    values = [data.get(t) for t in tenors]
    if all(v is not None and v != '' for v in values):
        if values[0] > values[-1]:
            shape = 'inverted (near-term richer than long-term) - a backwardation-like shape, worth noting'
        elif min(values) == values[2] or min(values) == values[1]:
            shape = 'smile shape - dips around 20-30 days then rises toward longer tenors, a typical calm-market pattern'
        else:
            shape = 'generally rising with tenor - longer-dated options pricing more uncertainty than near-term, also typical'
        lines.append('Curve shape: ' + shape)

    contango = data.get('contango')
    if contango is not None and contango != '':
        if contango < 0:
            lines.append('Contango: NEGATIVE (' + str(round(contango, 4)) + ') - backwardation, historically associated with market stress')
        else:
            lines.append('Contango: positive (' + str(round(contango, 4)) + ') - normal term structure')

    slopepctile = data.get('slopepctile')
    if slopepctile is not None and slopepctile != '':
        cat = categorize(slopepctile)
        lines.append('Slope percentile: ' + str(slopepctile) + ' (' + cat + ' vs its own 1yr range per ORATS standard low/moderate/high bands)')

    ivpctile = data.get('ivPctile1y')
    if ivpctile is not None and ivpctile != '':
        cat = categorize(ivpctile)
        lines.append('IV percentile 1yr: ' + str(ivpctile) + ' (' + cat + ')')

    slope = data.get('slope')
    slopeFcst = data.get('slopeFcst')
    if slope is not None and slopeFcst is not None and slope != '' and slopeFcst != '':
        if slopeFcst > slope:
            lines.append('Slope forecast (' + str(slopeFcst) + ') is ABOVE current slope (' + str(slope) + ') - ORATS model expects skew to steepen, historically favors risk-reversal strategies per University 203')
        else:
            lines.append('Slope forecast (' + str(slopeFcst) + ') is BELOW current slope (' + str(slope) + ') - ORATS model expects skew to flatten, historically favors collar strategies per University 203')

    slopeInf = data.get('slopeInf')
    if slope is not None and slopeInf is not None and slope != '' and slopeInf != '':
        if slopeInf > slope:
            lines.append('Slope (near-term, ' + str(slope) + ') vs slopeInf (long-dated, ' + str(slopeInf) + '): long-dated skew is steeper. Per general options market convention (not ORATS-specific), near-term skew is normally the steeper of the two - this inverted pattern can indicate acute near-term fear has eased while longer-horizon uncertainty remains relatively elevated')
        else:
            lines.append('Slope (near-term, ' + str(slope) + ') vs slopeInf (long-dated, ' + str(slopeInf) + '): near-term skew is steeper, the normal/typical relationship per general options market convention, consistent with acute near-term risk being priced higher than longer-horizon risk')

    for pair in [('fbfwd30_20','30/20'), ('fbfwd90_30','90/30')]:
        field, label = pair
        val = data.get(field)
        if val is not None and val != '':
            if abs(val - 1.0) > 0.05:
                lines.append('Forward ratio ' + label + ': ' + str(val) + ' - notable divergence from 1.0, per ORATS this has historically foreshadowed larger moves')
            else:
                lines.append('Forward ratio ' + label + ': ' + str(val) + ' - close to 1.0, no anomaly flagged')
            if val > 1.0:
                lines.append('  fbfwd ratio above 1.0: consistent with low-vol regime, historically associated with buying volatility strategies')
            else:
                lines.append('  fbfwd ratio below 1.0: consistent with high-vol regime, historically associated with selling volatility strategies')

    lines.append('')
    lines.append('Note: this commentary describes what the data shows, it is not a trade recommendation.')
    return chr(10).join(lines)

if __name__ == '__main__':
    run_check()
