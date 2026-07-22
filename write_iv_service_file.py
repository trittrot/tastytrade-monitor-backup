content = "[Unit]\nDescription=ETF IV Percentile Checker\nAfter=network.target\n\n[Service]\nType=simple\nUser=mike\nWorkingDirectory=/home/mike/tastytrade-monitor\nExecStart=/home/mike/tastytrade-monitor/venv/bin/python3 -u /home/mike/tastytrade-monitor/etf_iv_percentile_alert.py\nRestart=always\nRestartSec=10\nStandardOutput=append:/home/mike/tastytrade-monitor/etf_iv_service.log\nStandardError=append:/home/mike/tastytrade-monitor/etf_iv_service.log\n\n[Install]\nWantedBy=multi-user.target\n"
with open('/tmp/etf-iv-alert.service', 'w') as f:
    f.write(content)
print("Service file written")
