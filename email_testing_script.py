import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email credentials
SMTP_SERVER = 'smtp.gmail.com'  # or your mail server
SMTP_PORT = 587
USERNAME = 'sakshamguptaopsb@gmail.com'
PASSWORD = 'igby cego snyb smjk'

# Email sending function
def send_email(to_address, subject, body):
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = to_address
    msg['Subject'] = subject

    # Attach body text
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, to_address, msg.as_string())
        print(f"Mail sent to {to_address} with subject {subject}")

# Main function to send 100 emails
def send_bulk_emails(recipient_email):
    for i in range(1, 101):  # Loop to send 100 emails
        subject = f"Load testing mail {i}"
        body = f"This is the body of load testing mail {i}"
        send_email(recipient_email, subject, body)

if __name__ == "__main__":
    # Define the recipient email
    recipient = 'amrc66283@gmail.com'

    # Send bulk emails
    send_bulk_emails(recipient)
