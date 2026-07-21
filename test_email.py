import smtplib
from email.mime.text import MIMEText
from secrets_loader import get_secret

def send_test_email():
    password = get_secret("miket-gmail-app-password").replace(" ", "")
    from_addr = get_secret("miket-email")
    to_addr = get_secret("mike-email")

    msg = MIMEText("This is a test email from your Tastytrade monitoring VM.")
    msg['Subject'] = "Tastytrade Monitor - Test Email"
    msg['From'] = from_addr
    msg['To'] = to_addr

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())

    print("Test email sent successfully")

if __name__ == "__main__":
    send_test_email()
