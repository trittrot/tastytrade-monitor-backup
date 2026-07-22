from datetime import datetime
from auth import authenticate_production
from alerts import send_alert

def run_heartbeat():
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    try:
        session = authenticate_production()
        msg = f"Tastytrade monitor heartbeat OK - {today}"
        print(msg)
        return True
    except Exception as e:
        msg = f"Tastytrade monitor heartbeat FAILED - {today} - {e}"
        print(msg)
        send_alert(msg)
        return False

if __name__ == "__main__":
    run_heartbeat()
