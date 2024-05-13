import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_alert_email(receiver, Subject, message, user_name):
    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['From'] = 'freshcart.appv2@gmail.com'
    msg['To'] = receiver
    msg.attach(MIMEText(generate_email(Subject, message, user_name), 'html'))

    smtp_server = 'smtp.gmail.com'
    port = 587
    smtp_user = 'freshcart.appv2@gmail.com'
    smtp_pass = 'injkfjekxtbkefaw'

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail('freshcart.appv2@gmail.com', receiver, msg.as_string())

def generate_email(subject, message, user_name):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}

            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}

            .header {{
                background-color: #007bff;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}

            .content {{
                padding: 20px;
                text-align: center;
            }}

            .footer {{
                background-color: #f4f4f4;
                padding: 10px;
                text-align: center;
            }}

            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #007bff;
                color: #ffffff;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{subject}</h1>
            </div>
            <div class="content">
                <p>Hello {user_name},</p>
                <p>{message}</p>
                <p>Thank you for using our service!</p>
                <a href="http://localhost:8080/" class="button">View Details</a>
            </div>
            <div class="footer">
                <p>This is an automated notification. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html_content
