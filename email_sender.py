import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
PORT = int(os.getenv("SMTP_PORT"))

def send_email(to_email, name, body, attachment_paths=[]):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = f"Hi {name}, here's something for you"

    msg.attach(MIMEText(body, "plain"))

    # Attach files
    for path in attachment_paths:
        filename = os.path.basename(path)
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=filename)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
        print(f"✅ Email sent to {name}")
    except Exception as e:
        print(f"❌ Failed to send to {name} - {e}")
