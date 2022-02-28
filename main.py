from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
import requests
from classes.classes import Sender, Checker
from pydantic import EmailStr
import random

app = FastAPI(doc_url='/docs', redoc_url='/doc')


def send_pic(email: str, rqst: str):

    r = requests.get(f'https://imsea.herokuapp.com/api/1?q={rqst}')
    nmb = 1
    randlist = []
    if not (r.json()['results']):
        Sender.send_error(email)
        return None
    while len(randlist) != 5:
        randlist.append(random.randrange(0, (len(r.json()['results']))))
    for i in randlist:
        pic = requests.get((r.json()['results'][i]))
        with open(f'images/picture{nmb}.jpg', 'wb') as file:
            file.write(pic.content)
        nmb += 1
    Sender.send(email)


@app.get('/search')
async def req(background: BackgroundTasks, email: EmailStr, rqst: str = Depends(Checker.check_rqst)):
    background.add_task(send_pic, email, rqst)
    return JSONResponse('Данные отправлены по email')
