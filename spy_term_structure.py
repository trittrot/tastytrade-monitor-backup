import urllib.request
import json
import csv
import os
from datetime import date
from secrets_loader import get_secret

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
    print('Logged ' + str(len(FIELD_ORDER)) + ' fields for ' + today)

def print_summary(data):
    print('=== SPY Term Structure - ' + data.get('tradeDate','') + ' ===')
    print('Confidence: ' + str(data.get('confidence','')))
    print()
    print('Ex-earnings IV curve:')
    print('  10d: ' + str(data.get('exErnIv10d','')) + '  20d: ' + str(data.get('exErnIv20d','')) + '  30d: ' + str(data.get('exErnIv30d','')))
    print('  60d: ' + str(data.get('exErnIv60d','')) + '  90d: ' + str(data.get('exErnIv90d','')))
    print('  6m: ' + str(data.get('exErnIv6m','')) + '  1y: ' + str(data.get('exErnIv1y','')))
    print()
    print('Contango: ' + str(data.get('contango','')))
    print()
    print('Forward curve: fwd30_20=' + str(data.get('fwd30_20','')) + '  fwd90_30=' + str(data.get('fwd90_30','')))
    print('Forward anomaly check: fbfwd30_20=' + str(data.get('fbfwd30_20','')) + '  fbfwd90_30=' + str(data.get('fbfwd90_30','')))
    print()
    print('Slope: ' + str(data.get('slope','')) + '  Slope percentile: ' + str(data.get('slopepctile','')))
    print('Slope forecast: ' + str(data.get('slopeFcst','')))
    print('IV percentile 1y: ' + str(data.get('ivPctile1y','')))
    print('IV/HV ratio: ' + str(data.get('ivHvXernRatio','')))

if __name__ == '__main__':
    data = fetch_term_structure()
    print_summary(data)
    log_term_structure(data)
