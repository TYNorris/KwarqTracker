import logging
import smtplib
import ssl

from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.src.config import get_config

logger = logging.getLogger(__name__)
config = get_config()


class Emailer:
    def __init__(self):
        self.address = config.EMAIL_ADDRESS
        self.password = config.EMAIL_PASSWORD
        self.smtp_server = "smtp.gmail.com"

    def send_email(self, receivers, message: MIMEMultipart):
        try:
            with smtplib.SMTP_SSL(self.smtp_server) as server:
                server.set_debuglevel(1)
                server.login(self.address, self.password)

                for receiver in receivers:
                    message["To"] = receiver
                    server.sendmail(self.address, receiver, message.as_string())
                    logger.info(f"Sent today's attendance to {receiver}")

        except Exception:
            logger.exception("Failed to send email")

    def send_attendance(self, names: list):
        message = MIMEMultipart()
        today = date.today().strftime(f"%m/%d/%y")

        body = "Here is the KwarQs attendance for today."

        for name in names:
            body += f"\n\t- {name}"

        message["From"] = config.EMAIL_ADDRESS
        message["Subject"] = f"Attendance for {today}"
        message.attach(MIMEText(body))

        self.send_email(config.DESTINATION_ADDRESSES, message)

