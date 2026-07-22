content = "import json\nimport csv\nimport os\nimport smtplib\nfrom email.mime.text import MIMEText\nfrom datetime import date, datetime\nfrom auth import authenticate_production\nfrom alerts import send_alert\nfrom secrets_loader import get_secret\n\nLOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'es_iv_percentile_log.csv')\nTHRESHOLD = 80.0\n\ndef fetch_es_iv_metrics():\n    session = authenticate_production()\n    data = session._get('/market-metrics?symbols=/ES')\n    metrics = data['items'][0]\n    iv_pctile = float(metrics['implied-volatility-percentile']) * 100\n    iv_rank = float(metrics['implied-volatility-index-rank']) * 100\n    return iv_pctile, iv_rank\n"
with open('es_iv_percentile_alert.py', 'w') as f:
    f.write(content)
print("Chunk 1 written")
