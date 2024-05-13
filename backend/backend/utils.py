from email.mime.application import MIMEApplication
import os
from flask import render_template_string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib




def send_email(receiver, Subject, message, user_name):
    """
    Send an email with customizable HTML content.
    """
    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['From'] = 'themusic.nine@gmail.com'
    msg['To'] = receiver
    msg.attach(MIMEText(generate_email_content(Subject, message, user_name), 'html'))

    smtp_server = 'smtp.gmail.com'
    port = 587
    smtp_user = 'themusic.nine@gmail.com'
    smtp_pass = 'ybxlcntaesgzncrs'

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail('themusic.nine@gmail.com', receiver, msg.as_string())



def send_activity_summary_email(receiver, subject, data):
    """
    Send a monthly activity summary email.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'themusic.nine@gmail.com'
    msg['To'] = receiver
    msg.attach(MIMEText(generate_activity_summary_email(data), 'html'))

    smtp_server = 'smtp.gmail.com'
    port = 587
    smtp_user = 'themusic.nine@gmail.com'
    smtp_pass = 'ybxlcntaesgzncrs'

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail('themusic.nine@gmail.com', receiver, msg.as_string())

def send_export_complete_email(subject, email, attachment_path):
    """
    Send an email notification with an attached CSV file.
    """
    msg = MIMEMultipart()
    msg['Subject'] = 'CSV Export Complete'
    msg['From'] = 'themusic.nine@gmail.com'
    msg['To'] = email
    msg.attach(MIMEText("The product CSV export is complete."))


    with open(attachment_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name=attachment_path)
    part['Content-Disposition'] = f'attachment; filename="{attachment_path.split("/")[-1]}"'
    msg.attach(part)

    smtp_server = 'smtp.gmail.com'
    port = 587
    smtp_user = 'themusic.nine@gmail.com'
    smtp_pass = 'ybxlcntaesgzncrs'

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail('themusic.nine@gmail.com', email, msg.as_string())

def generate_activity_summary_email(data):
    """
    Generate HTML content for the monthly activity summary email.
    """
    html_template = """
    <html>
        <head>
            <style>
                body {font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}
                .container {max-width: 600px; margin: auto; background: #f0f0f0; padding: 20px;}
                h2 {color: #007BFF;}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Monthly Music Activity Summary</h2>
                <p>Here's how you rocked last month:</p>
                <ul>
                    {% for song in data %}
                        <li>{{ song.name }} by {{ song.singer }}: Played {{ song.play_count }} times</li>
                    {% endfor %}
                </ul>
                <p>Keep the music playing!</p>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_template, data=data)


def generate_email_content(subject, message, user_name):
    """
    Generate HTML content for a customizable email.
    """
    return f"""
    <html>
        <head>
            <style>
                body {{font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}}
                .container {{max-width: 600px; margin: auto; background: #f0f0f0; padding: 20px;}}
                h2 {{color: #007BFF;}}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>{subject}</h2>
                <p>Dear {user_name},</p>
                <p>{message}</p>
                <p>Best wishes,</p>
                <p>Your Music Player Team</p>
            </div>
        </body>
    </html>
    """
def send_activity_summary_email(receiver, subject, data):
    """
    Send a monthly activity summary email to a user.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'yourmusicapp@example.com'  # This should be your actual "from" email address
    msg['To'] = receiver
    # The MIMEText part generates the email's body. Here, `generate_activity_summary_email` is called
    # with `data`, which should be structured according to your needs (e.g., a list of song plays).
    msg.attach(MIMEText(generate_activity_summary_email(data), 'html'))

    smtp_server = 'smtp.example.com'  # Your SMTP server
    port = 587  # Common port for SMTP
    smtp_user = 'themusic.nine@gmail.com'
    smtp_pass = 'ybxlcntaesgzncrs'

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Start TLS encryption
        server.login(smtp_user, smtp_pass)  # Log in to the SMTP server
        server.sendmail(smtp_user, receiver, msg.as_string())  # Send the email

def generate_activity_summary_email(data):
    """
    Generate HTML content for the monthly activity summary email.
    """
    html_template = """
    <html>
        <head>
            <style>
                body {font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333;}
                .container {max-width: 600px; margin: auto; background: #f0f0f0; padding: 20px;}
                h2 {color: #007BFF;}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Monthly Music Activity Summary</h2>
                <p>Here's how you rocked last month:</p>
                <ul>
                    {% for song in data %}
                        <li>{{ song.name }} by {{ song.singer }}: Played {{ song.play_count }} times</li>
                    {% endfor %}
                </ul>
                <p>Keep the music playing!</p>
            </div>
        </body>
    </html>
    """
    # Render the HTML template with the provided data
    return render_template_string(html_template, data=data)
