from tastytrade import Session
from secrets_loader import load_all_secrets

def authenticate_production():
    secrets = load_all_secrets()
    session = Session(
        secrets["tastytrade_client_secret"],
        secrets["tastytrade_refresh_token"]
    )
    print("Connected to Production")
    return session
