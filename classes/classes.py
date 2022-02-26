from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from data_dict import data
import os

msg = MIMEMultipart()
server = smtplib.SMTP('smtp.gmail.com: 587')

password = data.get('Pass')
msg['From'] = data.get('Email')


class ApiException(Exception):
    pass


class Checker:
    @staticmethod
    def start():
        if not os.path.exists('data_dict.py'):
            raise ApiException('Нужно создать .py файл с данными в словаре')

        if not os.path.exists('images/'):
            os.mkdir('images/')


class Sender:

    @staticmethod
    def send_error(email):

        message = 'По запросу не найдено ни одного изображения.'

        msg['To'] = email
        msg['Subject'] = 'ImageSeaError'

        msg.attach(MIMEText(message, 'plain'))
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    @staticmethod
    def send(email):
        message = 'Картиночки завезли.'

        msg['To'] = email
        msg['Subject'] = 'ImageSea'

        msg.attach(MIMEText(message, 'plain'))
        with open('images/picture1.jpg', 'rb') as file:
            msg.attach(MIMEImage(file.read()))
        with open('images/picture2.jpg', 'rb') as file:
            msg.attach(MIMEImage(file.read()))
        with open('images/picture3.jpg', 'rb') as file:
            msg.attach(MIMEImage(file.read()))
        with open('images/picture4.jpg', 'rb') as file:
            msg.attach(MIMEImage(file.read()))
        with open('images/picture5.jpg', 'rb') as file:
            msg.attach(MIMEImage(file.read()))
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
