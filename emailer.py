import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date


def send_email(sender: str, app_password: str, recipient: str, html_body: str) -> None:
    """
    Sends the HTML newsletter via Gmail SMTP using an app password.

    Setup instructions (do this once):
    1. Go to myaccount.google.com → Security → 2-Step Verification (must be ON)
    2. Search "App passwords" → create one named "semis-newsletter"
    3. Use that 16-char password as GMAIL_APP_PASSWORD in your .env
    """
    subject = f"Semiconductor Daily Briefing — {date.today().strftime('%B %d, %Y')}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    recipients = [r.strip() for r in recipient.split(",")]  # support multiple recipients separated by commas
    msg["To"] = ", ".join(recipients)

    # Attach HTML body — Gmail will render it natively
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, recipients, msg.as_string())

    print(f"✓ Newsletter sent to {recipient}")