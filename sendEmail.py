import json
import os
from dotenv import load_dotenv
from datetime import datetime
import locale

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import markdown2

def load_trending_data_processed_Antrophic(file_path='trending_data_processed_Antrophic.json'):
    return load_trending_data_processed(file_path)

def load_trending_data_processed_OpenAI(file_path='trending_data_processed_OpenAI.json'):
    return load_trending_data_processed(file_path)

def load_trending_data_processed(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Warnung: Datei {file_path} nicht gefunden.")
        return


def format_number_de(value):
    """Formatiert eine Zahl im deutschen Stil mit Punkten als Tausendertrennzeichen."""
    return f"{value:,}".replace(",", ".")

def translate_started(started):
    """Übersetzt englische Zeitangaben ins Deutsche."""
    translations = {
        "hours": "Stunden",
        "hour": "Stunde",
        "minutes": "Minuten",
        "minute": "Minute",
        "days": "Tage",
        "day": "Tag"
    }
    for en, de in translations.items():
        if en in started:
            return started.replace(en, de)
    return started  # Fallback, falls keine Übersetzung gefunden wird


def create_email_object(data):
    # Lokale Einstellungen für die deutsche Sprache
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

    # Timestamp in ein deutsches Datumsformat umwandeln
    timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
    subject = f"Die deutschen Trends vom {timestamp.strftime('%d.%m.%Y %H:%M')}"

    # Body zusammenstellen
    body_lines = []
    for trend in data["processed_trends"]:
        trend_header = f"#### \"{trend['category']}\": \"{trend['trend']}\""
        suchvolumen = format_number_de(trend["searchvolume"])
        started_de = translate_started(trend["started"])
        suchvolumen = f"#### Suchvolumen: {suchvolumen} - {started_de}"
        topic = f"# {trend['topic']}"

        related_searches = " - ".join(trend["related_searches"])
        related_searches_line = f"#### {related_searches}"

        what_section = f"## WAS\n{trend['what']}"
        why_section = f"## WARUM\n{trend['why']}"

        # Trend block zusammenstellen
        trend_block = f"{trend_header}\n{suchvolumen}\n{topic}\n{related_searches_line}\n{what_section}\n{why_section}"
        body_lines.append(trend_block)

    body = "\n\n".join(body_lines)

    # Email-Objekt erstellen
    email_object = {
        "subject": subject,
        "body": body
    }

    return email_object

def main():
    # Umgebungsvariablen aus .env-Datei laden
    load_dotenv()
    trending_data_processed = json.loads(load_trending_data_processed_OpenAI())
    email_object = create_email_object(trending_data_processed)
    mail(email_object)

def mail(email_object):
    # Email credentials and details
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = os.environ.get("SMTP_PORT")
    email_sender = os.environ.get("EMAIL_SENDER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_recipient = os.environ.get("EMAIL_RECIPIENT")

    # Create the email
    subject = email_object['subject']
    body = markdown2.markdown(email_object['body'])

    # Build the email content
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = email_recipient
    message["Subject"] = subject

    # Attach the email body
    message.attach(MIMEText(body, "html"))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_recipient, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == "__main__":
    main()