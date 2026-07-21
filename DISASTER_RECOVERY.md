# Disaster Recovery Runbook - Tastytrade Monitoring System

If you are a future Claude instance reading this with no prior context: this document describes how to rebuild Mikes automated Tastytrade and ORATS monitoring system from scratch. Follow it step by step, one command at a time, waiting for confirmation before proceeding.

## System Overview
A Google Cloud Platform VM runs several scheduled Python scripts via cron and one continuous background service via systemd. These monitor markets and Mikes trading conditions, sending SMS alerts via Twilio and email via Gmail SMTP. The system is monitoring and alerting ONLY, it never places trades. Mike manually executes all trades himself.

## Prerequisites
Mike needs: access to Google Cloud account mike@tritton.net, Tastytrade API credentials, Twilio credentials, ORATS API token, Gmail app password for miket@tritton.net. These values live only in Secret Manager and are not in this document. Mike should keep a separate secure backup of these raw values, for example a password manager.

## Step 1: Recreate the GCP Project if needed
If the whole project is gone, create a new one. If only the VM is gone but the project survives, skip to Step 3.

## Step 2: Enable required APIs
Enable Secret Manager API, Compute Engine API, Cloud Resource Manager API.

## Step 3: Recreate secrets in Secret Manager
Create these secret names with the real values: tastytrade-client-secret, tastytrade-refresh-token, twilio-account-sid, twilio-auth-token, orats-api-token, miket-gmail-app-password.

## Step 4: Create the VM
gcloud compute instances create tastytrade-monitor-vm --zone=us-central1-a --machine-type=e2-micro --image-family=ubuntu-2204-lts --image-project=ubuntu-os-cloud --boot-disk-type=pd-standard --boot-disk-size=30GB

## Step 5: Grant VM access to secrets
Stop the VM, run gcloud compute instances set-service-account with scopes cloud-platform, restart the VM. Also grant Secret Manager Secret Accessor IAM role from Cloud Shell.

## Step 6: Set VM timezone
sudo timedatectl set-timezone Europe/London

## Step 7: Install packages
sudo apt update, then sudo apt install python3-pip python3-venv git tmux

## Step 8: Set up Python environment
Create folder tastytrade-monitor, create and activate a venv inside it, then pip install tastytrade twilio nest_asyncio google-cloud-secret-manager

## Step 9: Recreate script files
Restore these from the Git backup, not from memory: secrets_loader.py, auth.py, alerts.py, heartbeat.py, es_gap_check.py, es_close_capture.py, es_sunday_reopen_check.py, orats_contango_monitor.py, vix_live_monitor.py

## Step 10: Recreate cron schedule
Jobs Monday to Friday: heartbeat at 0700, es_gap_check at 0701, orats_contango_monitor at 2116, es_close_capture at 2200. Sunday only: es_sunday_reopen_check at 2300. Each job cds into tastytrade-monitor and runs the venv python3 interpreter against the script, logging output to a matching file.

## Step 11: Recreate the VIX live monitor systemd service
Create a service file at etc systemd system vix-monitor.service pointing at vix_live_monitor.py with Restart set to always. Run systemctl daemon-reload, enable, start.

## Step 12: Set up the vm shortcut in Cloud Shell
Add an alias in bashrc that runs gcloud compute ssh into the VM and attaches to a tmux session called main.

## Step 13: Verify everything
Test each script manually, confirm SMS and email delivery, confirm crontab shows all 5 jobs, confirm vix-monitor service is active.

## Known gaps
Script contents are not embedded here, only on the live VM, until Git backup exists. Credential values are not backed up outside Secret Manager. This document itself needs a durable home outside the VM, such as the same Git repository.

## Design philosophy to preserve
Monitoring and alerting only, never autonomous trade execution. End of day or near end of day decisions preferred over intraday reactivity, Mikes explicit preference from past experience of poor intraday decisions. SMS for short alerts, email for detailed information. Scripts should fail loudly by alerting, never fail silently.
