from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from data_dict import data
import os
from fastapi import HTTPException

msg = MIMEMultipart()
server = smtplib.SMTP('smtp.gmail.com: 587')

password = data.get('Pass')
msg['From'] = data.get('Email')


class ApiException(HTTPException):
    pass


class Checker:

    @classmethod
    def start(cls):
        if not os.path.exists('data_dict.py'):
            raise ApiException(status_code=403, detail='Нужно создать .py файл с данными в словаре')

        if not os.path.exists('images/'):
            os.mkdir('images/')

    @classmethod
    async def check_rqst(cls, rqst: str):
        cls.start()
        if len(rqst) > 60:
            raise HTTPException(status_code=400, detail='Слишком длинный запрос')
        return rqst


class Sender:

    @classmethod
    def send_error(cls, email: str):
        message = 'По запросу не найдено ни одного изображения.'

        msg['To'] = email
        msg['Subject'] = 'ImageSeaError'

        msg.attach(MIMEText(message, 'plain'))
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

    @classmethod
    def send(cls, email: str):
        message = 'Картиночки завезли.'
        names = ('images/picture1.jpg', 'images/picture2.jpg', 'images/picture3.jpg', 'images/picture4.jpg', 'images/picture5.jpg')

        msg['To'] = email
        msg['Subject'] = 'ImageSea'

        msg.attach(MIMEText(message, 'plain'))
        for i in names:
            with open(i, 'rb') as file:
                msg.attach(MIMEImage(file.read()))
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
