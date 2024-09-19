import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
import os

# Email credentials
SMTP_SERVER = 'smtp.gmail.com'  # or your mail server
SMTP_PORT = 587
USERNAME = 'sakshamguptaopsb@gmail.com'
PASSWORD = 'igby cego snyb smjk'
# Email sending function
def send_email(to_address, subject, body, inline_image_path, attachment_path):
    # Set up the MIME
    msg = MIMEMultipart('related')  # 'related' allows embedding images in HTML
    msg['From'] = USERNAME
    msg['To'] = to_address
    msg['Subject'] = subject

    # Create the HTML part of the email with an image reference
    html_body = f"""
    <html>
    <body>
        <p>{body}</p>
        <p>Here is an inline image:</p>
        <img src="cid:inline_image">
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    # Attach inline image (Local File Path)
    if inline_image_path and os.path.exists(inline_image_path):
        with open(inline_image_path, 'rb') as f:
            mime_image = MIMEImage(f.read())
            mime_image.add_header('Content-ID', '<inline_image>')  # Use this ID in the HTML part
            mime_image.add_header('Content-Disposition', 'inline')  # Ensure the image is inline
            msg.attach(mime_image)

    # Attachment (Local File Path)
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(attachment_path)}',
            )
            msg.attach(part)

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, to_address, msg.as_string())
        print(f"Mail sent to {to_address} with subject {subject}")

# Main function to send 100 emails
def send_bulk_emails(recipient_email, inline_image_path, attachment_path):
    for i in range(1, 5):  # Loop to send 100 emails
        subject = f"Load testing mail {i}"
        body = f"This is the body of load testing mail {i}"
        send_email(recipient_email, subject, body, inline_image_path, attachment_path)

if __name__ == "__main__":
    # Define the recipient email, inline image, and attachment paths
    recipient = 'amrc66283@gmail.com'
    inline_image = r'C:\Users\sahil\OneDrive\Desktop\load_testing_opsbeat\load_image.png'
    attachment = r'C:\Users\sahil\OneDrive\Desktop\load_testing_opsbeat\load_attach.txt'  

    # Send bulk emails
    send_bulk_emails(recipient, inline_image, attachment)
