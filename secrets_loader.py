from google.cloud import secretmanager

PROJECT_ID = "tastytrade-monitor-v1"

def get_secret(secret_id, project_id=PROJECT_ID):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def load_all_secrets():
    return {
        "tastytrade_client_secret": get_secret("tastytrade-client-secret"),
        "tastytrade_refresh_token": get_secret("tastytrade-refresh-token"),
        "twilio_account_sid": get_secret("twilio-account-sid"),
        "twilio_auth_token": get_secret("twilio-auth-token"),
        "orats_api_token": get_secret("orats-api-token"),
        "gmail_app_password": get_secret("miket-gmail-app-password"),
    }
