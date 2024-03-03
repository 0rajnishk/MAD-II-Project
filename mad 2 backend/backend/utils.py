from email.mime.application import MIMEApplication
from flask import render_template_string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


def send_email(receiver, Subject, message, user_name):
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

def send_monthly_email(data):
    msg = MIMEMultipart()
    msg['Subject'] = 'Monthly Report'
    msg['From'] = 'freshcart.appv2@gmail.com'
    msg['To'] = 'sunnikumar.arya@gmail.com'
    msg.attach(MIMEText(generate_monthly_email(data), 'html'))

    smtp_server = 'smtp.gmail.com'
    port = 587
    smtp_user = 'freshcart.appv2@gmail.com'
    smtp_pass = 'injkfjekxtbkefaw'

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail('freshcart.appv2@gmail.com', 'sunnikumar.arya@gmail.com', msg.as_string())

def send_export_complete_email():
    msg = MIMEMultipart()
    msg['Subject'] = 'CSV Export Complete'
    msg['From'] = 'freshcart.appv2@gmail.com'
    msg['To'] = 'sunnikumar.arya@gmail.com'
    msg.attach(MIMEText("The product CSV export is complete."))
    with open('exported_products.csv', 'rb') as f:
        part = MIMEApplication(f.read(), Name="exported_products.csv")
    part['Content-Disposition'] = f'attachment; filename="exported_products.csv"'
    msg.attach(part)

    smtp_server = 'smtp.gmail.com'
    port = 587
    smtp_user = 'freshcart.appv2@gmail.com'
    smtp_pass = 'injkfjekxtbkefaw'

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail('freshcart.appv2@gmail.com', 'harinivaishu1911@gmail.com', msg.as_string())

def generate_monthly_email(data):
    # HTML template for the email
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }

            .container {
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            h2 {
                color: #333;
            }

            h3 {
                color: #555;
            }

            ul {
                list-style: none;
                padding: 0;
            }

            li {
                margin-bottom: 10px;
            }

            p {
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Monthly Report</h2>
            
            {% for user, orders in data.items() %}
                <h3>{{ user }}</h3>
                <ul>
                    {% for order in orders %}
                        <li> For Order Id : {{ order.id }} - Total Price : {{ order.total_price }}</li>
                    {% endfor %}
                </ul>
            {% endfor %}

            <p>Thank you for using our service!</p>
        </div>
    </body>
    </html>

    """

    # Render the HTML template with the provided data
    html_content = render_template_string(html_template, data=data)

    return html_content

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