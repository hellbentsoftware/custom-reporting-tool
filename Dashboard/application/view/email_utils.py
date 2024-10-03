import smtplib
import pdfkit
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from config import EMAIL_CREDENTIALS

def send_dashboard_email(email, pdf_filename="dashboard.pdf"):
    sender_email, sender_password = EMAIL_CREDENTIALS['email'], EMAIL_CREDENTIALS['password']
    
    subject = "Your Dashboard PDF"
    body = "Please find the attached dashboard PDF."
    
    # Create email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    # Attach PDF
    with open(pdf_filename, "rb") as attachment:
        part = MIMEApplication(attachment.read(), _subtype="pdf")
        part.add_header("Content-Disposition", "attachment", filename=pdf_filename)
        message.attach(part)

    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        return f"Dashboard sent to {email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"

def generate_pdf_from_url(url, output_filename):
    path_wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url(url, output_filename, configuration=config)
