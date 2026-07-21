from twilio.rest import Client
from secrets_loader import get_secret

def send_alert(message_text):
    try:
        account_sid = get_secret("twilio-account-sid")
        auth_token = get_secret("twilio-auth-token")
        from_number = get_secret("twilio-from-number")
        to_number = get_secret("mike-mobile-number")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_text,
            from_=from_number,
            to=to_number
        )
        print(f"Alert sent (SID: {message.sid})")
        return True
    except Exception as e:
        print(f"ALERT FAILED TO SEND: {e}")
        return False
