content = "[Unit]\nDescription=ETF Confidence Scanner\nAfter=network.target\n\n[Service]\nType=simple\nUser=mike\nWorkingDirectory=/home/mike/tastytrade-monitor\nExecStart=/home/mike/tastytrade-monitor/venv/bin/python3 -u /home/mike/tastytrade-monitor/etf_confidence_scan.py\nRestart=always\nRestartSec=10\nStandardOutput=append:/home/mike/tastytrade-monitor/etf_confidence_service.log\nStandardError=append:/home/mike/tastytrade-monitor/etf_confidence_service.log\n\n[Install]\nWantedBy=multi-user.target\n"
with open('/tmp/etf-confidence-scan.service', 'w') as f:
    f.write(content)
print("Service file written to /tmp")
