import smtplib
import ssl
from email.mime.text import MIMEText
import aiomisc
from textwrap import dedent

from core.settings import settings
from db import models


class EmailManager:
    @staticmethod
    def send(msg, user):
        msg['To'] = user.email
        msg['From'] = settings.email_login

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
            s.login(settings.email_login, settings.email_password)
            s.send_message(msg)

    @aiomisc.threaded
    def send_link_to_change_password(self, user: models.User, action: models.ChangePassword):
        msg = MIMEText(dedent(f"""\
            {user.first_name}, ссылка для смены пароля: {action.value}
        """), _charset="UTF-8")
        msg['Subject'] = "Ссылка для смены пароля"
        self.send(msg, user)

    @aiomisc.threaded
    def send_email_with_new_password(self, user: models.User, pwd: str):
        msg = MIMEText(f"{user.first_name}, вот пароль {pwd}", _charset="UTF-8")
        msg['Subject'] = "Временный пароль"

        self.send(msg, user)
