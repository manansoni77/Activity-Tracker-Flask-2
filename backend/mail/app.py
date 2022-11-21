from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from os.path import basename

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'todoapp@gmail.com'
SENDER_PASSWORD = ''

def send_email(to_address, subject, message, attachments = []):
    msg = MIMEMultipart()
    msg['To'] = to_address
    msg['From'] = SENDER_ADDRESS
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))

    for (file, name) in attachments:
        file.seek(0)
        part = MIMEApplication(file.read(), name=name)
        part['Content-Disposition'] = f'attachment; filename="{name}"'
        msg.attach(part)

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT)
    s.login(user = SENDER_ADDRESS, password = SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True