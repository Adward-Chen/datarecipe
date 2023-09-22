import smtplib
from email.mime.text import MIMEText

def send_email(subject: str, body: str, send_emial_address:str, send_emial_password:str, receive_email_address: str, smtp_address:str='smtp.feishu.cn', smtp_port:int=465):
    # For SMTP, the email and password
    PASSWORD = send_emial_password  # Password

    msg = MIMEText(body)
    msg['From'] = send_emial_address
    msg['To'] = receive_email_address
    msg['Subject'] = subject

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL(smtp_address, smtp_port) as server:  # Using SMTP_SSL to connect
        server.login(send_emial_address, PASSWORD)
        server.sendmail(send_emial_address, receive_email_address, msg.as_string())
