import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

load_dotenv()  
Mail_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,  # Your Gmail address
    MAIL_PASSWORD=Mail_PASSWORD,                       # Your Gmail password or app password
    MAIL_FROM=MAIL_USERNAME,      # Sender email
    MAIL_PORT=587,                                  # SMTP port for TLS
    MAIL_SERVER="smtp.gmail.com",                   # Gmail SMTP server
    MAIL_STARTTLS=True,                             # Enable STARTTLS
    MAIL_SSL_TLS=False,                             # Disable SSL/TLS (use STARTTLS instead)
    USE_CREDENTIALS=True,                           # Enable authentication
    VALIDATE_CERTS=True                             # Validate SSL certificates
)