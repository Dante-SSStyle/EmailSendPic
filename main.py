from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
import requests
from classes.classes import Sender, Checker
from data_dict import data

app = FastAPI(doc_url='/docs', redoc_url='/doc')
send = Sender()
check = Checker()


async def check_email(email: str):
    check.start()
    true_email = data.get('TrueEmail')
    if email != true_email:
        raise HTTPException(status_code=403, detail='Доступ запрещён.')
    return email


def send_pic(email: str, rqst: str):

    r = requests.get(f'https://imsea.herokuapp.com/api/1?q={rqst}')
    nmb = 1
    if not (r.json()['results']):
        send.send_error(email)
        return None
    for i in range(0, 9, 2):
        pic = requests.get((r.json()['results'][i]))
        with open(f'images/picture{nmb}.jpg', 'wb') as file:
            file.write(pic.content)
        nmb += 1
    send.send(email)


@app.post('/search')
async def req(rqst: str, background: BackgroundTasks, email: str = Depends(check_email)):
    if len(rqst) > 60:
        raise HTTPException(status_code=400, detail='Слишком длинный запрос')
    background.add_task(send_pic, email, rqst)
    response = '200 OK'
    return response
