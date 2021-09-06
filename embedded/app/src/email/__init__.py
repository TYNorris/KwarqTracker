import logging
import smtplib

from datetime import date
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from app.src.config import get_config
from app.src.user.user import User

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

    def send_attendance(self, names: List[str], all_users: List[User]):
        message = MIMEMultipart()
        today = date.today().strftime(f"%m-%d-%y")

        body = "Here is the KwarQs attendance for today."

        for name in names:
            body += f"\n\t- {name}"

        message["From"] = config.EMAIL_ADDRESS
        message["Subject"] = f"Attendance for {today}"
        message.attach(MIMEText(body))

        csv = self.make_csv(all_users)
        attachment = MIMEText(csv)
        attachment.add_header('Content-Disposition',
                              'attachment',
                              filename=f'kwarqs{today}.csv')

        message.attach(attachment)
        self.send_email(config.DESTINATION_ADDRESSES, message)

    def make_csv(self, all_users: List[User]):
        all_dates = set()
        for user in all_users:
            for d in user.dates_attended:
                if d not in all_dates:
                    all_dates.add(d)

        date_list = list(all_dates)
        date_list.sort()
        date_list = [str(d) for d in date_list]

        csv = "Name, " + ", ".join(date_list)
        csv += "\n"

        for user in all_users:
            csv += f"{user.name}, "
            for d in date_list:
                if date.fromisoformat(d) in user.dates_attended:
                    csv += "x, "
                else:
                    csv += " , "
            csv += "\n"

        return csv



