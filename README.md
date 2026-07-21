# Tastytrade Monitoring System - Backup Repository

This repository is a backup of Mikes automated Tastytrade and ORATS monitoring system, which normally runs on a Google Cloud VM.

See DISASTER_RECOVERY.md for the full step by step guide to rebuilding the system from scratch if the VM is ever lost.

This system is monitoring and alerting ONLY. It never places trades automatically. All trade decisions and execution are made manually by Mike via the Tastytrade platform.

## Key scripts
secrets_loader.py - retrieves credentials from Google Secret Manager
auth.py - authenticates to Tastytrade
alerts.py - sends SMS alerts via Twilio
heartbeat.py - daily system alive check
es_gap_check.py - morning ES futures gap check
es_close_capture.py - evening ES futures close capture
es_sunday_reopen_check.py - Sunday reopen gap check
orats_contango_monitor.py - daily ORATS contango reading and alert
vix_live_monitor.py - continuous intraday VIX threshold monitor, runs as a systemd service

Most other files are exploratory test scripts used while evaluating the ORATS API and are lower priority to restore.
