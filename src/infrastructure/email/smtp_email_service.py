import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.application.ports.email_service import EmailService

# Usar variables de entorno en producción
class SMTPEmailService(EmailService):
    def __init__(self, host: str, port: int, user: str, password: str, from_email: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.from_email = from_email

    async def send_email(self, to: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to
            
            part = MIMEText(body, "html")
            msg.attach(part)
            
            # Since this is an async method but smtplib is sync,
            # In a real app we'd use aiosmtplib. Here we fake the await or run in executor
            # For brevity, standard smtplib setup:
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.from_email, to, msg.as_string())
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
