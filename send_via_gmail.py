import os
import sys
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, html_file, to_email):
    sender = os.environ.get("GMAIL_SENDER")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not app_password:
        print("ERROR: GMAIL_SENDER and GMAIL_APP_PASSWORD environment variables must be set.")
        sys.exit(1)

    if not os.path.exists(html_file):
        print(f"ERROR: File {html_file} does not exist.")
        sys.exit(1)

    with open(html_file, 'r') as f:
        html_content = f.read()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    print(f"Connecting to Gmail SMTP...")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, to_email, msg.as_string())

    print(f"Email sent successfully to {to_email}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send newsletter via Gmail SMTP")
    parser.add_argument("--type", choices=["daily", "weekly"], required=True, help="Type of newsletter to send")
    parser.add_argument("--to", required=True, help="Recipient email address")

    args = parser.parse_args()

    if args.type == "daily":
        subject = "L&A Consulting Daily Intelligence"
        html_file = "output/daily_brief.html"
    else:
        subject = "L&A Consulting Weekly Digest"
        html_file = "output/weekly_digest.html"

    send_email(subject, html_file, args.to)
